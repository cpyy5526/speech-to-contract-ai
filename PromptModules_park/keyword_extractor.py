from openai import OpenAI
from typing import Callable
from dotenv import load_dotenv, find_dotenv
import os
import json
from keyword_schema import keyword_schema

load_dotenv(find_dotenv())
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)


# 임시 호출 함수/ 이후 메인 모듈의 gpt 호출 함수로 대체 되어야함
def call_gpt_api(prompt):
    return client.chat.completions.create(model="gpt-4", messages = prompt, temperature = 0.2)

def generate_contract(
    contract_type: str,
    conversation: str,
    gpt_caller: Callable[[list[dict]], str]  # dict들의 리스트를 인자로 받아 문자열을 리턴하는 함수
) -> str:
    
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

    prompt = f"""
        다음은 작성된 계약에 관한 대화입니다.

        ## 대화 내용:
        {conversation}

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
        """






    messages = [{"role": "system", "content": "당신은 계약서를 분석하는 법률 전문가 AI입니다."},
                {"role": "user", "content": prompt}]
    response = gpt_caller(messages)
    result = response.choices[0].message.content.strip()

    return result

# ✅ FastAPI 제거하고, 스크립트 실행 시 계약서 생성하도록 변경
if __name__ == "__main__":
    test_conversation = """
        야, 나 이번에 급하게 돈이 좀 필요해서 그러는데 혹시 도와줄 수 있어?

        얼마 정도 필요한데?

        2천만 원 정도. 급전이 필요해서 대출 알아봤는데 승인도 오래 걸리고 이율도 너무 높더라.

        2천이면 적지 않은 돈인데... 빌려주는 건 어렵지 않은데 그냥 무상으로 해줄 순 없고, 이자 정도는 받아야 해.

        알지 알지. 당연히 이자는 드려야지. 요즘 기준으로 보면 몇 퍼센트 정도 잡아야 해?

        법정이율이 5%니까 그 정도면 적당할 것 같아. 1년에 5%면 2천 기준으로 100만 원이지.

        그럼 매달 이자 내는 걸로 하면 월 8만 3천 원 정도 되겠네.

        맞아. 원금은 1년 뒤에 일시상환하고, 이자는 매달 말일에 주는 걸로 하자.

        좋아. 혹시 담보는 필요해? 지금은 따로 세울 게 없어서...

        담보는 괜찮아. 대신 신용으로 하는 거니까 확실하게 지켜줘야 해.

        알겠습니다. 그럼 차용증은 꼭 써야겠죠?

        당연하지. 나중에 괜히 서로 불편해지는 일 없게 기본적인 건 다 명시해야 해. 대여금액, 이자율, 지급 방식, 상환 기한, 연체이자율 이런 거.

        연체이자율은 어떻게 잡을까? 보통 얼마로 해?

        대개는 약정이율의 1.5배에서 2배 정도 잡는데, 우리끼리 하는 거니까 10%로 하자. 그래도 연체하면 부담은 있어야지.

        오케이. 그리고 이거 혹시 공증도 받아야 할까?

        금액이 막 억단위도 아니고, 우리 사이도 있으니까 공증까지는 안 해도 될 것 같아. 대신 문자나 이메일로 주고받은 기록은 남겨두자.

        알겠어. 그럼 오늘 안으로 차용증 작성하고, 계좌번호 주면 바로 이체 받을게.

        좋아. 계좌번호 보낼게. 준비되면 얘기해.

        정말 고마워. 1년 안에 깔끔하게 정리할게.

        믿고 빌려주는 거니까 서로 깔끔하게 가자.
        """

    contract_type = "소비대차"
    print(generate_contract(contract_type, test_conversation, call_gpt_api))
