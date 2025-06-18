from app.core.logger import logging
logger = logging.getLogger(__name__)

from pathlib import Path
from sqlalchemy.orm import Session

from app.core.celery_app import celery_app
from app.db.session import get_sync_session

from app.models.transcription import Transcription
from app.models.generation import Generation, GenerationStatus
from app.models.contract import Contract
from app.models.suggestion import GptSuggestion

from app.core.llm import call_gpt_api
from app.core.config import settings
from app.prompts.type_classifier import get_contract_type
from app.prompts.keyword_extractor import extract_fields
from app.prompts.annotater import annotate_contract_text
from app.prompts.keyword_schema import (
    is_supported_contract_type, matches_schema, is_valid_field_path
)


@celery_app.task(name="tasks.generations.process_generation_pipeline", bind=True)
def process_generation_pipeline(self, generation_id: str) -> None:
    logger.info("계약서 생성 파이프라인 시작: generation_id=%s", generation_id)

    session = get_sync_session()
    try:
        # 생성된 generation 레코드 가져오기
        generation = session.get(Generation, generation_id)
        if not generation or generation.status in {
            GenerationStatus.cancelled, GenerationStatus.done
        }:
            return

        # join. transcription 레코드 가져오기 (-> script_file uuid 가져오기)
        transcription = session.get(
            Transcription,
            generation.transcription_id
        )
        if not transcription or not transcription.script_file:
            generation.status = GenerationStatus.failed
            session.commit()
            return
        
        # 1. 계약 유형 판단
        session.refresh(generation)
        if generation.status == GenerationStatus.cancelled:
            return
        contract_type = get_contract_type(
            transcription.script_file,
            call_gpt_api
        )
        ### 정의되지 않은 계약 유형인 경우 생성 실패 처리
        if not is_supported_contract_type(contract_type):
            generation.status = GenerationStatus.failed
            session.commit()
            logger.error("Unsupported contract type generated: \'%s\'", contract_type)
            return
        logger.debug("계약 유형 판별 완료: type='%s'", contract_type)

        # 2. 계약서 JSON 생성
        session.refresh(generation)
        if generation.status == GenerationStatus.cancelled:
            return
        contract_fields = extract_fields(
            transcription.script_file,
            contract_type,
            call_gpt_api
        )
        ### 생성된 JSON 필드 유효성 검증
        if not matches_schema(contract_type, contract_fields):
            generation.status = GenerationStatus.failed
            session.commit()
            logger.error("Generated contract fields do not match schema for type \'%s\'", contract_type)
            return
        logger.debug("계약서 JSON 필드 추출 완료: 필드 수=%d", len(contract_fields))

        # 3. 공란에 대한 정보 제안 텍스트 생성
        session.refresh(generation)
        if generation.status == GenerationStatus.cancelled:
            return
        contract_suggestions = annotate_contract_text(
            contract_type,
            contract_fields,
            call_gpt_api
        )

        # 계약서 테이블에 새 레코드 추가
        contract = Contract(
            user_id=generation.user_id,
            generation_id=generation.id,
            contract_type=contract_type,
            contents=contract_fields,
            initial_contents=contract_fields,
        )
        session.add(contract)
        session.commit()  # 먼저 commit하여 contract.id 생성

        # 계약서 필드마다 제안 텍스트를 suggestion 테이블에 새 레코드로 추가
        for field_path, suggestion_text in contract_suggestions.items():
            # 유효하지 않은 key에 대한 제안은 저장하지 않고 로그만 남김
            if not is_valid_field_path(contract_type, field_path):
                logger.warning("Invalid suggestion field_path: \'%s\'", field_path)
                continue
            if suggestion_text.strip():  # 빈 제안은 저장하지 않음
                suggestion = GptSuggestion(
                    contract_id=contract.id,
                    field_path=field_path,
                    suggestion_text=suggestion_text,
                )
                session.add(suggestion)

        # 계약서 생성 파이프라인 성공적으로 완료
        generation.status = GenerationStatus.done
        session.commit()
        logger.info("계약서 생성 파이프라인 완료: generation_id=%s", generation.id)

        # 대화 텍스트 삭제
        try:
            script_path = Path(settings.TEXT_UPLOAD_DIR) / transcription.script_file
            if script_path.is_file():
                script_path.unlink()
                logger.debug("Deleted script file after successful generation: %s", script_path)
        except Exception as e:
            logger.warning("Failed to delete script file %s: %s", script_path, e)

    # 계약서 생성 파이프라인 실패 및 중단
    except Exception as exc:
        logger.exception("계약서 생성 파이프라인 실패: generation_id=%s", generation_id)
        try:
            if "generation" in locals() and generation:
                generation.status = GenerationStatus.failed
                session.commit()
        except Exception as e:
            logger.warning("generation 상태 저장 중 추가 에러 발생: %s", e)
        raise exc

    finally:
        session.close()