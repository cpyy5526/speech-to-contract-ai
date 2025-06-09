from __future__ import annotations
from app.core.logger import logging
logger = logging.getLogger(__name__)

import logging
from typing import List, Dict
from openai import OpenAI

from app.core.config import settings


class GPTCallError(Exception):
    """GPT 호출 실패 시 발생하는 예외."""

# 전역 싱글턴 클라이언트
_client = OpenAI(
    api_key=settings.OPENAI_API_KEY,
    base_url=settings.OPENAI_API_BASE,
    timeout=settings.OPENAI_TIMEOUT,
)


def call_gpt_api(messages: List[Dict[str, str]]) -> str:
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
    logger.debug("GPT 요청 시작. 메시지 길이=%d", settings.OPENAI_MODEL, len(messages))

    try:
        response = _client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=messages,
            temperature=settings.OPENAI_TEMPERATURE,
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
