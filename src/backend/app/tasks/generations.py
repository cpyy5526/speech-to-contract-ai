import asyncio
from uuid import UUID

from app.core.celery_app import celery_app
from app.db.session import async_session

from app.models.transcription import Transcription
from app.models.generation import Generation, GenerationStatus
from app.models.contract import Contract
from app.models.suggestion import GptSuggestion

from app.core.llm import call_gpt_api
from app.prompts.type_classifier import get_contract_type
from app.prompts.keyword_extractor import extract_fields
from app.prompts.annotater import annotate_contract_text


@celery_app.task(name="tasks.generations.process_generation_pipeline")
def process_generation_pipeline(generation_id: str) -> None:
    async def _run(gid: UUID):
        async with async_session() as session:
            try:
                # 생성된 generation 레코드 가져오기
                generation = await session.get(Generation, gid)
                if not generation or generation.status in {
                   GenerationStatus.cancelled, GenerationStatus.done
                }:
                    return

                # join. transcription 레코드 가져오기 (-> script_file uuid 가져오기)
                transcription = await session.get(
                    Transcription,
                    generation.transcription_id
                )
                if not transcription or not transcription.script_file:
                    generation.status = GenerationStatus.failed
                    await session.commit()
                    return
                
                # 계약 유형 판단
                contract_type = await get_contract_type(
                    transcription.script_file,
                    call_gpt_api
                )

                # 계약서 JSON 생성
                contract_fields = await extract_fields(
                    transcription.script_file,
                    contract_type,
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
                await session.commit()  # 먼저 commit하여 contract.id 생성

                # 공란에 대한 정보 제안 텍스트 생성
                contract_suggestions = await annotate_contract_text(
                    contract_type,
                    contract_fields,
                    call_gpt_api
                )

                # 계약서 필드마다 제안 텍스트를 suggestion 테이블에 새 레코드로 추가
                for field_path, suggestion_text in contract_suggestions.items():
                    if suggestion_text.strip():  # 빈 제안은 저장하지 않음
                        suggestion = GptSuggestion(
                            contract_id=contract.id,
                            field_path=field_path,
                            suggestion_text=suggestion_text,
                        )
                        session.add(suggestion)

                # 계약서 생성 파이프라인 성공적으로 완료
                generation.status = GenerationStatus.done
                await session.commit()

            # 계약서 생성 파이프라인 실패 및 중단
            except Exception as exc:
                generation.status = GenerationStatus.failed
                await session.commit()
                raise exc

    asyncio.run(_run(UUID(generation_id)))