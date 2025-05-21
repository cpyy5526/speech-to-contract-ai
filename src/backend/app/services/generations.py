from __future__ import annotations

"""
app/services/generations.py
===========================

계약서 **생성** 비즈니스 로직.

* Whisper 변환 결과(스크립트 파일) → GPT 파이프라인 실행
* contracts_contents / gpt_suggestions 테이블에 데이터 영속화
* 생성 상태 조회‧취소 지원

   이 모듈은 GPT 호출을 직접 구현하지 않습니다.
   프롬프트 팀 함수에 `call_gpt_api`(의존성 주입)만 전달합니다.
"""

from datetime import datetime
from pathlib import Path
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.contract import Contract, GenerationStatus
from app.models.suggestion import GptSuggestion
from app.models.transcription import Transcription, TranscriptionStatus
from app.schemas.generation import GenerationStatusResponse

# 프롬프트 팀 모듈 – 내부 구현은 알 수 없음 (호출만 수행)
from app.prompts.contract_generation import (
    classify_contract_type,
    extract_keywords,
    generate_contract,
    suggest_missing_fields,
)

# 중앙 GPT 호출 함수 (DI 방식)
from app.core.llm import call_gpt_api  # type: ignore

__all__ = [
    # public API
    "generate_contract",
    "get_generation_status",
    "cancel_generation",
    # exceptions
    "TranscriptionNotReady",
    "NoAudioData",
    "NoGenerationInProgress",
    "CannotCancelGeneration",
    "DatabaseError",
]


# --------------------------------------------------------------------------- #
# Exceptions
# --------------------------------------------------------------------------- #
class TranscriptionNotReady(Exception):
    """Transcription 상태가 *done* 이 아니거나 스크립트 파일이 없을 때."""


class NoAudioData(Exception):
    """사용자에게 Transcription 레코드 자체가 없을 때."""


class NoGenerationInProgress(Exception):
    """진행 중인 계약서 생성이 전혀 없을 때."""


class CannotCancelGeneration(Exception):
    """현재 단계에서 생성 취소가 불가능할 때."""


class DatabaseError(Exception):
    """SQLAlchemy 예외 래퍼."""


# --------------------------------------------------------------------------- #
# 내부 헬퍼
# --------------------------------------------------------------------------- #
async def _latest_transcription(session: AsyncSession) -> Transcription | None:
    stmt = (
        select(Transcription)
        .order_by(Transcription.created_at.desc())
        .limit(1)
    )
    res = await session.execute(stmt)
    return res.scalar_one_or_none()


async def _latest_contract(session: AsyncSession) -> Contract | None:
    stmt = select(Contract).order_by(Contract.created_at.desc()).limit(1)
    res = await session.execute(stmt)
    return res.scalar_one_or_none()


def _to_response(contract: Contract) -> GenerationStatusResponse:
    return GenerationStatusResponse(
        status=contract.generation_status.value  # enum → str
        if hasattr(contract.generation_status, "value")
        else str(contract.generation_status),
        contract_id=str(contract.id),
    )


# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #
async def generate_contract(session: AsyncSession) -> GenerationStatusResponse:
    """
    Whisper 텍스트를 이용해 계약서를 생성하고 DB에 저장합니다.

    Flow
    ----
    1. 최신 Transcription 확인 (done)
    2. 스크립트 파일 로드
    3. GPT 파이프라인 실행
    4. contracts_contents & gpt_suggestions 저장
    5. 상태 done 으로 마무리
    """
    try:
        transcription = await _latest_transcription(session)
        if transcription is None:
            raise NoAudioData
        if transcription.status != TranscriptionStatus.done:
            raise TranscriptionNotReady
        if not transcription.script_file:
            raise TranscriptionNotReady

        # 1) 스크립트 파일 읽기
        script_path = Path(transcription.script_file)
        if not script_path.exists():
            raise TranscriptionNotReady
        text: str = script_path.read_text(encoding="utf-8")

        # 2) GPT 프롬프트 체인
        contract_type: str = await classify_contract_type(text, call_gpt_api)
        keywords: dict = await extract_keywords(text, contract_type, call_gpt_api)
        contract_data: dict = await generate_contract(keywords, call_gpt_api)
        suggestions: list[dict] = await suggest_missing_fields(contract_data, call_gpt_api)

        # 3) 계약서 레코드 생성 (generating → done)
        contract = Contract(
            user_id=transcription.user_id,
            contract_type=contract_type,
            contents=contract_data,
            initial_contents=contract_data,
            generation_status=GenerationStatus.generating,
        )
        session.add(contract)
        await session.commit()
        await session.refresh(contract)

        # 4) GPT 제안 텍스트 저장
        for s in suggestions:
            session.add(
                GptSuggestion(
                    contract_id=contract.id,
                    field_path=s.get("field_path", ""),
                    suggestion_text=s.get("suggestion_text", ""),
                )
            )

        # 5) 상태 done 저장
        contract.generation_status = GenerationStatus.done
        contract.updated_at = datetime.utcnow()
        session.add(contract)
        await session.commit()
        await session.refresh(contract)

        return _to_response(contract)

    except (TranscriptionNotReady, NoAudioData):
        raise
    except SQLAlchemyError as exc:
        await session.rollback()
        raise DatabaseError from exc
    except Exception:
        # 예기치 못한 오류 발생 시 상태를 failed 로 남김
        try:
            if "contract" in locals():
                contract.generation_status = GenerationStatus.failed
                contract.updated_at = datetime.utcnow()
                session.add(contract)
                await session.commit()
        finally:
            raise


async def get_generation_status(session: AsyncSession) -> GenerationStatusResponse:
    """가장 최근 계약서 생성의 진행 상황을 반환합니다."""
    try:
        contract = await _latest_contract(session)
        if contract is None:
            raise NoGenerationInProgress
        return _to_response(contract)
    except NoGenerationInProgress:
        raise
    except SQLAlchemyError as exc:
        raise DatabaseError from exc


async def cancel_generation(session: AsyncSession) -> None:
    """generating 상태인 계약서 생성을 취소합니다."""
    try:
        contract = await _latest_contract(session)
        if contract is None:
            raise NoGenerationInProgress
        if contract.generation_status != GenerationStatus.generating:
            raise CannotCancelGeneration

        contract.generation_status = GenerationStatus.cancelled
        contract.updated_at = datetime.utcnow()
        session.add(contract)
        await session.commit()
    except (NoGenerationInProgress, CannotCancelGeneration):
        raise
    except SQLAlchemyError as exc:
        await session.rollback()
        raise DatabaseError from exc
