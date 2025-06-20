from pathlib import Path

from app.core.celery_app import celery_app
from app.db.session import get_sync_session
from app.core.stt import transcribe_audio
from app.models.transcription import Transcription, TranscriptionStatus
from app.prompts.preprocessor import text_preprocess
from app.core.config import settings

from app.core.logger import logging
logger = logging.getLogger(__name__)


@celery_app.task(name="tasks.transcriptions.process_uploaded_audio", bind=True)
def process_uploaded_audio(self, transcription_id: str) -> None:
    logger.info("STT 태스크 시작: transcription_id=%s", transcription_id)

    session = get_sync_session()
    try:
        transcription = session.get(Transcription, transcription_id)
        if not transcription or transcription.status in {
            TranscriptionStatus.cancelled,
            TranscriptionStatus.done,
        }:
            return

        # 상태: transcribing
        transcription.status = TranscriptionStatus.transcribing
        session.commit()
        logger.info("transcription 상태 'transcribing' 설정 완료: transcription_id=%s", transcription_id)

        try:
            # Whisper API 호출 및 변환
            script_filename = transcribe_audio(transcription.audio_file)
            processed_filename = f"processed_{script_filename}"

            # 텍스트 전처리 실행
            text_preprocess(script_filename, processed_filename)

        except Exception as exc:
            transcription.status = TranscriptionStatus.transcription_failed
            session.commit()
            logger.error("STT 변환 실패: transcription_id=%s", transcription.id, exc_info=True)
            raise exc
        else:
            updated_transcription = session.get(Transcription, transcription_id)
            if updated_transcription.status == TranscriptionStatus.cancelled:
                return
            
            # Transcription 테이블 레코드에 파일명 저장하고 상태 반영
            transcription.script_file = processed_filename
            transcription.status = TranscriptionStatus.done
            session.commit()
            logger.info(
                "STT 및 전처리 완료: transcription_id=%s, 파일=%s",
                transcription.id, processed_filename
            )

            # 음성파일 삭제
            try:
                audio_path= Path(settings.AUDIO_UPLOAD_DIR) / transcription.audio_file
                if audio_path.is_file():
                    audio_path.unlink()
                    logger.debug("Deleted audio file after successful transcription: %s", audio_path)
            except Exception as e:
                    logger.warning("Failed to delete audio file %s: %s", audio_path, e)
                    
    finally:
        session.close()
