from __future__ import annotations

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

__all__ = [
    "create_generation",
    "get_generation_status",
    "cancel_generation",
    "retry_generation",
]


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

async def create_generation(user_id: UUID, session: AsyncSession) -> None:
    """Register a new *Generation* and enqueue the GPT pipeline.

    Flow
    ----
    1. 가장 최근 *Transcription* 레코드가 **done** 상태인지 확인
    2. 같은 transcription 이 이미 generation 에 연결돼 있으면 409
    3. 동시에 진행 중인 generation 이 있으면 409
    4. 새 *Generation* 레코드(status="generating") 저장 및 commit
    5. Celery 태스크 큐에 `process_generation_pipeline` 등록
    """

    transcription = await _latest_finished_transcription(user_id, session)

    # 해당 transcription 이 이미 사용됐다면 재사용 불가 → 404 로 음성 데이터 없음 취급
    existing = await session.exec(
        select(Generation).where(Generation.transcription_id == transcription.id)
    )
    if existing.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No audio data for this user",
        )

    # 동시에 다른 generation 이 진행 중이라면 충돌 방지
    latest_gen = await _get_latest_generation(user_id, session, raise_if_none=False)
    if latest_gen and latest_gen.status == GenerationStatus.generating:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Generation already in progress",
        )

    generation = Generation(
        user_id=user_id,
        transcription_id=transcription.id,
        status=GenerationStatus.generating,
    )

    try:
        session.add(generation)
        await session.commit()
        await session.refresh(generation)
    except SQLAlchemyError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected server error",
        )

    # Celery background task
    process_generation_pipeline.delay(str(generation.id))


async def get_generation_status(
    user_id: UUID, session: AsyncSession
) -> GenerationStatusResponse:
    """현재 사용자의 가장 최근 Generation 상태를 반환합니다."""

    generation = await _get_latest_generation(user_id, session)

    response = GenerationStatusResponse(status=generation.status.value)

    if generation.status == GenerationStatus.done:
        # 방어적으로 가장 최근 계약서를 조회 (1:1 매핑 설계가 아니라면 타임스탬프로 식별)
        result = await session.exec(
            select(Contract)
            .where(Contract.user_id == user_id)
            .order_by(Contract.created_at.desc())
            .limit(1)
        )
        contract = result.first()
        if contract:
            response.contract_id = str(contract.id)

    return response


async def cancel_generation(user_id: UUID, session: AsyncSession) -> None:
    """생성 파이프라인을 중단하고 상태를 *cancelled* 로 전환합니다."""

    generation = await _get_latest_generation(user_id, session)

    if generation.status not in {
        GenerationStatus.generating,
        GenerationStatus.failed,
    }:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Cannot cancel generation at this stage",
        )

    generation.status = GenerationStatus.cancelled
    await session.commit()


async def retry_generation(user_id: UUID, session: AsyncSession) -> None:
    """*failed* 상태인 Generation 을 재시도합니다."""

    generation = await _get_latest_generation(user_id, session)

    if generation.status != GenerationStatus.failed:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Cannot retry generation at this stage",
        )

    generation.status = GenerationStatus.generating
    await session.commit()

    process_generation_pipeline.delay(str(generation.id))


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

async def _latest_finished_transcription(
    user_id: UUID, session: AsyncSession
) -> Transcription:
    """가장 최근 *done* 상태의 Transcription 이 없으면 404/409 예외."""

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
    """사용자의 최신 Generation 레코드 조회."""

    try:
        result = await session.exec(
            select(Generation)
            .where(Generation.user_id == user_id)
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
