from app.core.celery_app import celery_app
from backend.app.services import contracts
from app.models import Transcription, Contract
from app.db.session import get_async_session
from backend.app.services import generations, transcriptions

@celery_app.task
def transcribe_audio(transcription_id: str) -> None:
    async with get_async_session() as session:
        tr: Transcription = await session.get(Transcription, transcription_id)
        tr.status = Status.transcribing
        await session.commit()

        # 1. 파일 읽기
        audio_path = contracts.get_audio_path(tr.audio_file)
        # 2. Whisper 호출
        try:
            script_file = transcriptions.run(audio_path)
            tr.script_file = script_file
            tr.status = Status.done
        except Exception:
            tr.status = Status.transcription_failed
        finally:
            await session.commit()

@celery_app.task
def generate_contract(contract_id: str) -> None:
    # Whisper 결과 파일을 열어 GPT 호출
    ...