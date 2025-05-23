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

        ## [검토 대상 키워드]
        {json.dumps(filtered_fields, indent=2, ensure_ascii=False)}

        아래 지시사항에 따라 단계적 사고하고, 최종 결과는 반드시 위 JSON 구조와 동일한 형식으로 출력하세요.

        ---

        ## 1단계: 각 항목의 값을 확인합니다.
        - 항목의 값이 공란("")인지 확인합니다.

        ## 2단계: 공란("")인 경우, 다음의 [각 키워드별 공란 시 문제점]을 바탕으로 해당 항목이 빠졌을 때 발생할 수 있는 법적 문제를 설명합니다.
        - 반드시 다음과 같은 형식으로 작성하세요:  
            **"공란일 경우 ~ 수 있습니다."** (예: 공란일 경우 계약 효력이 부정될 수 있다.)
        - 반드시 **"공란일 경우"**로 시작하는 문장만 작성합니다.

        ## [각 키워드별 공란 시 문제점]
        {keyword_review_info}

        ## 3단계: 공란이 아닌 경우, 절대 어떤 판단도 하지 않고 해당 항목은 빈 문자열("")로 출력합니다.
        - 값이 있는 항목에 대해 절대 코멘트를 작성하지 않습니다.

        ## 4단계: 아래 조건에 따라 최종 JSON을 출력합니다.
        - 출력 결과는 반드시 위에 정의된 JSON 구조(계층, 필드명, 형식 포함)를 그대로 따라야 합니다.
        - 정의된 JSON 구조 이외의 dict 형태나 중첩 구조는 절대 허용하지 않습니다.
        - 반드시 JSON 형식으로만 출력하세요.
        - 모든 key와 value는 **이중 따옴표(")** 를 사용합니다.
        - 단일 따옴표(')는 절대 사용하지 않습니다.
        - **JSON 외의 설명, 해석, 단계 내용, 안내 문구는 절대 포함하지 않습니다.**
        - 오직 JSON 결과만 출력하세요.
        - JSON 이외의 텍스트가 포함되면 계약서로서 무효입니다.
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
        "contract_type": "소비대차",
        "loan_amount": {
            "amount_korean": "",
            "amount_number": "10,000,000"
        },
        "creditor": {
            "name": "김채권",
            "id_number": "",
            "address": "",
            "contact": "010-1111-2222"
        },
        "debtor": {
            "name": "",
            "id_number": "800202-2345678",
            "address": "",
            "contact": "010-3333-4444"
        },
        "interest": {
            "rate": "",
            "payment_method": "매월 말일에 계좌이체",
            "payment_date": ""
        },
        "repayment": {
            "repayment_date": "2025-12-31",
            "repayment_method": "일시 상환",
            "repayment_location": "",
            "account_info": ""
        },
        "special_terms": "연체 시 연 10%의 지연이자를 추가로 부과하며, 조기 상환은 수수료 없이 가능하다.",
        "contract_date": "",
        "signature_and_seal": ""
    }
    print(annotate_contract_text("소비대차", extract_fields, call_gpt_api))