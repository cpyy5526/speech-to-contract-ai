from typing import Protocol

class GPTClient(Protocol):
    async def generate_contract(self, transcript: str) -> dict: ...
    async def suggest_fields(self, contract_json: dict) -> list[dict]: ...

class OpenAIClient:
    def __init__(self, openai_api_key: str):
        ...
    async def generate_contract(self, transcript: str) -> dict:
        # 실제 OpenAI 호출
        ...
    async def suggest_fields(self, contract_json: dict) -> list[dict]:
        ...

# 의존성 주입
def get_gpt_client() -> GPTClient:
    return OpenAIClient(settings.openai_key)