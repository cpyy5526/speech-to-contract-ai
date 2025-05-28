from __future__ import annotations

import logging
from typing import List, Dict, Any

from openai import AsyncOpenAI, AsyncError  # type: ignore

from app.core.config import settings

__all__ = ["call_gpt_api", "GPTCallError"]

logger = logging.getLogger(__name__)


class GPTCallError(Exception):
    """GPT 호출 실패 시 발생하는 예외."""


# 전역 싱글턴 클라이언트
_client = AsyncOpenAI(
    api_key=settings.OPENAI_API_KEY,
    base_url=settings.OPENAI_API_BASE or "https://api.openai.com/v1",
)


async def call_gpt_api(messages: List[Dict[str, str]]) -> str:
    """
    OpenAI Chat Completion API를 호출하여 응답 메시지 content를 반환합니다.

    Parameters
    ----------
    messages : list[dict[str, str]]
        OpenAI Chat 형식의 message 목록 (role, content).

    Returns
    -------
    str
        첫 번째 choice의 message.content

    Raises
    ------
    GPTCallError
        API 호출 오류, 파싱 오류 등 모든 실패 상황.
    """
    logger.debug("GPT 요청 시작 | 모델=%s | 메시지 수=%d", settings.OPENAI_MODEL, len(messages))

    try:
        response: Any = await _client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=messages,
            timeout=settings.OPENAI_TIMEOUT or 30,
        )
        logger.debug("GPT 응답 수신 완료")
    except Exception as exc:  # pylint: disable=broad-except
        logger.exception("GPT 호출 중 오류 발생: %s", exc)
        raise GPTCallError("Failed to call GPT API") from exc

    try:
        return response.choices[0].message.content.strip()  # type: ignore[attr-defined]
    except (AttributeError, IndexError, KeyError) as exc:
        logger.exception("GPT 응답 파싱 실패: %s", exc)
        raise GPTCallError("Invalid response structure from GPT API") from exc
