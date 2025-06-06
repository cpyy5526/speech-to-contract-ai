# 계약서 키워드 추출 모듈

import json, os, aiofiles
from typing import Callable, List, Dict, Awaitable

from app.prompts.keyword_schema import keyword_schema
from app.core.config import settings
    
# 대화 내용에서 계약서 필드를 JSON 형식으로 추출하기
async def extract_fields(
    script_filename: str,
    contract_type: str,
    gpt_caller: Callable[[List[Dict[str, str]]], Awaitable[str]]
    ) -> dict:
    
    schema = keyword_schema.get(contract_type, {})
    
    # selected_keys 생성
    selected_keys = []
    def extract_keys(prefix, d):
        for k, v in d.items():
            full_key = f"{prefix}.{k}" if prefix else k
            if isinstance(v, dict):
                extract_keys(full_key, v)
            else:
                selected_keys.append(full_key)
    extract_keys("", schema)
    
    # keyword_descriptions 생성
    def flatten_descriptions(prefix, d):
        flat = {}
        for k, v in d.items():
            full_key = f"{prefix}.{k}" if prefix else k
            if isinstance(v, dict):
                flat.update(flatten_descriptions(full_key, v))
            else:
                flat[full_key] = v
        return flat

    keyword_descriptions = flatten_descriptions("", schema)
    keyword_info = "\n".join(
        f"- `{key}`: {desc}" for key, desc in keyword_descriptions.items() if key in selected_keys
    )

    file_path = os.path.join(settings.TEXT_UPLOAD_DIR, script_filename)
    async with aiofiles.open(file_path, 'r', encoding='utf-8') as f:
        conversation_text = await f.read()

    prompt = f"""
        다음은 작성된 계약에 관한 대화입니다.

        ## 대화 내용:
        {conversation_text}

        ## 각 키워드의 의미:
        {keyword_info}

        아래 지시사항에 따라 단계적으로 사고하고, 최종 결과는 반드시 위 JSON 구조와 동일한 형식으로 작성하세요.

        ## 1단계: 대화 내용을 해석하여 핵심 사실을 파악합니다.
        - 누가 누구에게 무엇을 제공하는지, 금액, 기한, 조건 등을 이해합니다.

        ## 2단계: 각 키워드 의미를 기준으로 대화에서 필요한 정보를 도출합니다.
        - 대화 내용과 키워드 의미를 비교하며, 해당하는 정보를 찾습니다.

        ## 3단계: 최종 결과를 아래 조건에 맞게 JSON 구조로 출력합니다.
        - 출력 결과는 반드시 위에 정의된 JSON 구조(계층, 필드명, 형식 포함)를 그대로 따라야 합니다.
        - 정의된 JSON 구조 이외의 dict 형태나 중첩 구조는 절대 허용하지 않습니다.
        - 대화에 없는 값은 공란("")으로 채웁니다.
        - 반드시 JSON 형식으로만 출력하세요.
        - 모든 key와 value는 이중 따옴표(")를 사용합니다.
        - 단일 따옴표(')는 절대 사용하지 않습니다.
        - JSON 외의 설명, 해석, 단계 내용, 안내 문구는 절대 포함하지 않습니다.
        - 오직 JSON 결과만 출력하세요.
        - JSON 이외의 텍스트가 포함되면 계약서로서 무효입니다.
        - 날짜는 반드시 'YYYY-MM-DD' 형식으로 작성합니다. '오늘' 같은 표현은 허용하지 않습니다.
        """

    messages = [{"role": "system", "content": "당신은 계약서를 분석하는 법률 전문가 AI입니다."},
                {"role": "user", "content": prompt}]
    result = await gpt_caller(messages)

    try:
        return json.loads(result)
    except json.JSONDecodeError as e:
        raise ValueError(f"GPT 응답에서 JSON 파싱 실패:\n{result}\n\n에러: {e}")