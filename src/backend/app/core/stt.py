from __future__ import annotations

import uuid, aiofiles, logging
from pathlib import Path
from openai import AsyncOpenAI, OpenAIError

from app.core.config import settings  # type: ignore

__all__ = ["transcribe_audio", "STTCallError"]

logger = logging.getLogger(__name__)

# --------------------------------------------------------------------------- #
# Exceptions
# --------------------------------------------------------------------------- #

class STTCallError(RuntimeError):
    """Raised when a Whisper STT API call fails."""


# --------------------------------------------------------------------------- #
# OpenAI Whisper Client (global singleton)
# --------------------------------------------------------------------------- #

_client: AsyncOpenAI | None = None


def _get_client() -> AsyncOpenAI:
    """Create (once) and return an AsyncOpenAI client instance."""
    global _client
    if _client is None:
        _client = AsyncOpenAI(
            api_key=settings.OPENAI_API_KEY,  # loaded from .env
            base_url=settings.OPENAI_API_BASE,
            timeout=settings.OPENAI_TIMEOUT,
        )
        logger.debug("AsyncOpenAI client initialized for Whisper STT")
    return _client


# --------------------------------------------------------------------------- #
# Internal API
# --------------------------------------------------------------------------- #

async def transcribe_audio(audio_filename: str) -> str:
    """
    Convert an audio file to text using OpenAI Whisper.

    Parameters
    ----------
    path : str
        Absolute or project-relative path to an ``.mp3``/``.wav`` file stored on disk.

    Returns
    -------
    str
        The transcribed text.

    Raises
    ------
    STTCallError
        If the Whisper API call fails for any reason.
    """
    input_path = Path(settings.AUDIO_UPLOAD_DIR) / audio_filename
    if not input_path.is_file():
        raise STTCallError(f"Audio file not found: {input_path}")

    client = _get_client()

    try:
        logger.debug("Starting Whisper transcription for %s", input_path)
        # NOTE: ``file`` must be a binary file object
        async with input_path.open("rb") as fh:  # pyright: ignore[reportUnknownMemberType]
            response = await client.audio.transcriptions.create(
                model="whisper-1",
                file=fh,
                response_format="text",
            )

        text_out: str = response.strip() if isinstance(response, str) else response.text  # type: ignore[attr-defined]
        logger.debug("Finished Whisper transcription (%d chars)", len(text_out))

        # UUID filename 생성
        text_uuid = str(uuid.uuid4())
        output_filename = f"{text_uuid}.txt"
        output_path = Path(settings.TEXT_UPLOAD_DIR) / output_filename

        async with aiofiles.open(output_path, "w", encoding="utf-8") as f:
            await f.write(text_out)
        
        return output_filename

    except (OpenAIError, Exception) as exc:  # noqa: BLE001
        logger.exception("Whisper STT API call failed: %s", exc)
        raise STTCallError("Whisper STT API call failed") from exc
