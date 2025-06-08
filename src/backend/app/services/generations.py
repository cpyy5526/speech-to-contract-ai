from __future__ import annotations
from app.core.logger import logging
logger = logging.getLogger(__name__)

from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.transcription import Transcription, TranscriptionStatus
from app.models.generation import Generation, GenerationStatus
from app.models.contract import Contract
from app.schemas.generation import GenerationStatusResponse
from app.tasks.generations import process_generation_pipeline


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

async def create_generation(user_id: UUID, session: AsyncSession) -> None:
    """
    계약서 생성 추적을 위해 Generation 테이블에 레코드를 추가하거나
    기존 "failed" 레코드에 대해 재시도하고,
    비동기 Celery task queue에 계약서 생성 파이프라인을 등록합니다.
    """

    transcription = await _latest_finished_transcription(user_id, session)
    logger.info(
        "가장 최근 Transcription 조회 성공: user_id=%s, transcription_id=%s",
        user_id, transcription.id
    )

    # 해당 transcription이 이미 사용됨 (음성 업로드 및 변환 없이 요청, 과거에 이미 처리된 작업 조회됨)
    # 404로 음성 데이터 없음 취급
    existing = await session.exec(
        select(Generation).where(Generation.transcription_id == transcription.id)
    )
    if existing.first():
        logger.warning(
            "이미 사용된 transcription으로 생성 요청: user_id=%s, transcription_id=%s",
            user_id, transcription.id
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No audio data for this user",
        )

    latest_gen = await _get_latest_generation(user_id, session, raise_if_none=False)

    # 이미 해당 Transcription에 대한 Generation 레코드 존재
    if latest_gen:
        # "generating": 동일한 계약서 생성 파이프라인이 이미 실행 중, 충돌 방지
        if latest_gen.status == GenerationStatus.generating:
            logger.warning(
                "진행 중인 generation 존재: user_id=%s, generation_id=%s",
                user_id, latest_gen.id
            )
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Generation already in progress",
            )
        
        # "failed": 재시도 요청 발생, "generating"으로 업데이트 및 Celery 재등록
        elif latest_gen.status == GenerationStatus.failed:
            latest_gen.status = GenerationStatus.generating
            try:
                await session.commit()
                logger.info("실패한 generation 재시작: generation_id=%s", latest_gen.id)
            except SQLAlchemyError:
                await session.rollback()
                logger.error(
                    "generation 재시작 커밋 실패: generation_id=%s",
                    latest_gen.id, exc_info=True
                )
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Unexpected server error",
                )
            try:
                process_generation_pipeline.delay(str(latest_gen.id))
                logger.info(
                    "generation Celery 재등록 완료: generation_id=%s",
                    latest_gen.id
                )
            except Exception:
                logger.error(
                    "Celery 재등록 실패: generation_id=%s",
                    latest_gen.id, exc_info=True
                )
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Unexpected server error",
                )
            return

    # 새 Generation 레코드 객체 생성
    generation = Generation(
        user_id=user_id,
        transcription_id=transcription.id,
        status=GenerationStatus.generating,
    )

    # contracts_generations 테이블에 새 레코드 추가
    try:
        session.add(generation)
        await session.commit()
        await session.refresh(generation)
        logger.info("새 generation 레코드 생성 완료: generation_id=%s", generation.id)

    except SQLAlchemyError:
        await session.rollback()
        logger.error("generation 레코드 커밋 실패: user_id=%s", user_id, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected server error",
        )

    # Celery task queue에 계약서 생성 파이프라인 등록
    try:
        process_generation_pipeline.delay(str(generation.id))
        logger.info("generation Celery 등록 완료: generation_id=%s", generation.id)
    except Exception:
        logger.error("Celery 등록 실패: generation_id=%s", generation.id, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected server error",
        )


async def get_generation_status(
    user_id: UUID, session: AsyncSession
) -> GenerationStatusResponse:
    """현재 사용자의 가장 최근 Generation 상태를 반환합니다."""

    generation = await _get_latest_generation(user_id, session)
    logger.info(
        "generation 상태 조회 성공: user_id=%s, generation_id=%s, status=%s",
        user_id, generation.id, generation.status
    )

    response = GenerationStatusResponse(status=generation.status.value)

    # "done"인 경우 생성된 계약서 id도 함께 contract_contents 테이블에서 찾아 반환
    if generation.status == GenerationStatus.done:
        result = await session.exec(
            select(Contract)
            .where(Contract.generation_id == generation.id)
            .limit(1)
        )

        contract = result.first()
        if not contract:
            logger.error(
                "generation은 완료 상태이나 계약서 없음: generation_id=%s",
                generation.id
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Unexpected server error",
            )
        response.contract_id = str(contract.id)

        # 상태를 "archived"로 전환하여 추적 중이 아닌 "done" polling이 반복되지 않도록 막기
        generation.status = GenerationStatus.archived
        await session.commit()
        logger.debug("generation 상태 archived로 전환: generation_id=%s", generation.id)

    return response


async def cancel_generation(user_id: UUID, session: AsyncSession) -> None:
    """생성 파이프라인을 중단하고 상태를 "cancelled"로 전환합니다."""

    generation = await _get_latest_generation(user_id, session)

    if generation.status not in {
        GenerationStatus.generating,
        GenerationStatus.failed,
    }:
        logger.warning(
            "취소 불가한 generation 상태: user_id=%s, generation_id=%s, status=%s",
            user_id, generation.id, generation.status
        )
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Cannot cancel generation at this stage",
        )

    generation.status = GenerationStatus.cancelled
    await session.commit()
    logger.info("generation 취소 완료: generation_id=%s", generation.id)


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

async def _latest_finished_transcription(
    user_id: UUID, session: AsyncSession
) -> Transcription:
    """가장 최근 done 상태의 Transcription이 없으면 404/409 예외"""

    # 최신 transcription (존재해야 함)
    try:
        result = await session.exec(
            select(Transcription)
            .where(Transcription.user_id == user_id)
            .order_by(Transcription.created_at.desc())
            .limit(1)
        )
        transcription = result.first()
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected server error",
        )

    if not transcription:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No audio data for this user",
        )

    if transcription.status != TranscriptionStatus.done:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Transcription not ready",
        )

    return transcription


async def _get_latest_generation(
    user_id: UUID,
    session: AsyncSession,
    *,
    raise_if_none: bool = True,
) -> Generation:
    """사용자의 최신 Generation 레코드 조회"""

    try:
        result = await session.exec(
            select(Generation)
            .where(
                Generation.user_id == user_id,
                Generation.status != GenerationStatus.archived
            )
            .order_by(Generation.created_at.desc())
            .limit(1)
        )
        generation = result.first()
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected server error",
        )

    if not generation and raise_if_none:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No contract generation in progress",
        )

    return generation
