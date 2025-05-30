import json
from typing import Callable, List, Dict, Awaitable

from app.prompts.review_schema import contract_review_schema

# 입력 매개변수로 필요한 것 - 계약서 유형, 계약서 생성 모듈의 출력 json 결과
async def annotate_contract_text(
    contract_type: str,
    contract_fields: dict,
    gpt_caller: Callable[[List[Dict[str, str]]], Awaitable[str]]  # dict들의 리스트를 인자로 받아 문자열을 리턴하는 함수
) -> dict:
    
    schema = contract_review_schema.get(contract_type, {})

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

    # keyword_descriptions 생성, 반환값 정제
    def flatten(prefix, d):
        flat = {}
        for k, v in d.items():
            full_key = f"{prefix}.{k}" if prefix else k
            if isinstance(v, dict):
                flat.update(flatten(full_key, v))
            else:
                flat[full_key] = v
        return flat

    keyword_descriptions = flatten("", schema)
    keyword_review_info = "\n".join(
        f"- `{key}`: {desc}" for key, desc in keyword_descriptions.items() if key in selected_keys
    )
    
    filtered_fields = {}
    for key_path in selected_keys:
        parts = key_path.split(".")
        sub_data = contract_fields
        sub_result = filtered_fields

        for i, part in enumerate(parts):
            if isinstance(sub_data, dict) and part in sub_data:
                if i == len(parts) - 1:
                    # 마지막 키라면 값 할당
                    sub_result[part] = sub_data[part]
                else:
                    if part not in sub_result:
                        sub_result[part] = {}
                    sub_result = sub_result[part]
                    sub_data = sub_data[part]
            else:
                break  # 키가 없으면 무시

    prompt = f"""
        다음은 작성된 계약서에서 추출된 중요 키워드의 JSON 형식입니다. 

        각 항목의 값이 공란("")일 경우에만 법률적 관점에서 검토하고, 그에 따른 간단한 문제 설명을 작성해 주세요.
        값이 비어있지 않은 항목은 응답에서 빈 문자열("")로 남겨두고, 절대 코멘트하지 마세요.

        ❗주의사항:
        - 반드시 JSON 형식으로 출력하세요.
        - 모든 키(key)와 문자열 값(value)은 **이중 따옴표(")** 를 사용하세요.
        - **단일 따옴표(')** 는 절대 사용하지 마세요.
        - 응답에는 JSON 외의 설명, 해석, 안내 문구를 포함하지 마세요.
        - JSON 구조는 입력과 동일하게 유지해 주세요.

        [검토 대상 키워드]
        {json.dumps(filtered_fields, indent=2, ensure_ascii=False)}

        [각 키워드의 법적 의미 및 목적]
        {keyword_review_info}

        [지시사항]
        - 공란("")인 항목에 대해서만, 해당 키워드의 법적 의미를 참고해 발생할 수 있는 문제를 간단히 작성해 주세요.
        - 비어있지 않은 값은 빈 문자열("")로 출력하고, 관련 코멘트는 하지 마세요.
    """

    messages = [
        {
            "role": "system", 
            "content": (
                "당신은 법률 문서를 검토하는 전문가입니다. "
            )
        },
        {
            "role": "user", 
            "content": prompt
        }
    ]
    
    result = await gpt_caller(messages)
    
    try:
        suggestions = json.loads(result)
        return flatten("", suggestions)
    except json.JSONDecodeError as e:
        raise ValueError(f"❌ GPT 응답에서 JSON 파싱 실패:\n{result}\n\n에러: {e}")