from openai import OpenAI
from typing import Callable
from dotenv import load_dotenv, find_dotenv
import os
import json
from contract_review_schema import contract_review_schema

load_dotenv(find_dotenv())
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)


# 임시 호출 함수/ 이후 메인 모듈의 gpt 호출 함수로 대체 되어야함
def call_gpt_api(prompt):
    return client.chat.completions.create(model="gpt-4", messages = prompt, temperature = 0.2)


# 입력 매개변수로 필요한 것 - 계약서 유형, 계약서 생성 모듈의 출력 json 결과
def annotate_contract_text(
    contract_type: str,
    extract_fields: dict,
    gpt_caller: Callable[[list[dict]], str]  # dict들의 리스트를 인자로 받아 문자열을 리턴하는 함수
) -> str:
    
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
    keyword_review_info = "\n".join(
        f"- `{key}`: {desc}" for key, desc in keyword_descriptions.items() if key in selected_keys
    )
    
    filtered_fields = {}
    for key_path in selected_keys:
        parts = key_path.split(".")
        sub_data = extract_fields
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
    
    response = gpt_caller(messages)
    
    result = response.choices[0].message.content.strip()
    try:
        return json.loads(result)
    except json.JSONDecodeError:
        raise ValueError("GPT 응답에서 JSON 파싱 실패:\n" + result)







if __name__ == '__main__':
     #테스트용 extract_fields
    extract_fields = {
    "contract_type": "고용",
    "contract_name": "",
    "employer": {
        "company_name": "빅뷰",
        "representative_name": "",
        "address": "대현로 17",
        "contact": ""
    },
    "employee": {
        "name": "",
        "resident_number": "",
        "address": "",
        "contact": "010-4703-8256"
    },
    "employment_details": {
        "position": "",
        "duties": "",
        "workplace": "",
        "contract_period": {
        "start_date": "",
        "end_date": ""
        },
        "working_days": "",
        "working_hours": {
        "start_time": "",
        "end_time": "",
        "break_time": ""
        }
    },
    "wage_details": {
        "wage_type": "",
        "wage_amount": "",
        "payment_date": "",
        "payment_method": ""
    },
    "holidays": "",
    "social_insurance": {
        "national_pension": True,
        "health_insurance": True,
        "employment_insurance": True,
        "industrial_accident_insurance": True
    },
    "termination": "",
    "other_terms": "",
    "contract_date": "",
    "signature_and_seal": ""
    }
    print(annotate_contract_text("고용", extract_fields, call_gpt_api))