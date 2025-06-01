import asyncio
from uuid import UUID

from sqlmodel import select

from app.core.celery_app import celery_app
from app.db.session import async_session
from app.core.stt import transcribe_audio
from app.models.transcription import Transcription, TranscriptionStatus
from app.prompts.preprocessor import text_preprocess

@celery_app.task(name="tasks.transcriptions.process_uploaded_audio")
def process_uploaded_audio(transcription_id: str) -> None:
    """Whisper 기반 STT 변환 Celery 태스크."""

    async def _run(tid: UUID):
        async with async_session() as session:
            transcription = await session.get(Transcription, tid)
            if not transcription or transcription.status in {
                TranscriptionStatus.cancelled,
                TranscriptionStatus.done,
            }:
                return

            # 상태: transcribing
            transcription.status = TranscriptionStatus.transcribing
            await session.commit()

            try:
                # Whisper API 호출 및 변환
                script_filename = await transcribe_audio(transcription.audio_file)
                processed_filename = f"processed_{script_filename}"

                # 텍스트 전처리 실행
                await text_preprocess(script_filename, processed_filename)

            except Exception as exc:
                transcription.status = TranscriptionStatus.transcription_failed
                await session.commit()
                raise exc
            else:
                updated_transcription = await session.get(Transcription, tid)
                if updated_transcription.status == TranscriptionStatus.cancelled:
                    return
                
                transcription.script_file = processed_filename
                transcription.status = TranscriptionStatus.done
                await session.commit()

    asyncio.run(_run(UUID(transcription_id)))
