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
        - 날짜는 반드시 'YYYY-MM-DD' 형식으로 작성합니다. '오늘' 같은 표현은 허용하지 않습니다.
        """






    messages = [{"role": "system", "content": "당신은 계약서를 분석하는 법률 전문가 AI입니다."},
                {"role": "user", "content": prompt}]
    response = gpt_caller(messages)
    result = response.choices[0].message.content.strip()

    return result

# ✅ FastAPI 제거하고, 스크립트 실행 시 계약서 생성하도록 변경
if __name__ == "__main__":
    test_conversation = """
        요즘 현장 맡을 수 있는 여유 있으세요? 이번에 소규모 상가 리모델링 건이 하나 있는데, 내부 철거부터 마감까지 일괄로 맡길 분을 찾고 있어서요.

        공사 위치는 어디인가요?

        서울 강서구 쪽입니다. 공사명은 ‘○○상가 리모델링 공사’이고, 연면적은 350평 정도 됩니다.

        공사 기간은 어느 정도로 보시나요?

        6월 10일부터 시작해서 8월 31일까지 완료하는 걸 목표로 하고 있어요. 두 달 반 정도인데, 가능하시겠어요?

        그 정도면 충분합니다. 설계 도서는 완비된 상태인가요?

        네, 설계도서와 시방서는 다 준비되어 있습니다. 관련 자료는 계약서에 ‘설계도서 제21-05-리모델링’으로 명시할 예정입니다.

        공사 범위는 어디까지 포함되나요?

        기존 시설 철거, 내·외부 마감, 전기 배선 일부 재배치까지 포함입니다. 기계설비나 소방은 별도 발주입니다.

        총 공사금액은 얼마로 예상하고 계세요?

        부가세 포함해서 2억 2천만 원으로 보고 있습니다. 부가세는 포함 금액이고, 지급은 착공 시 20%, 중간 40%, 준공 후 40%로 3회 분할 예정입니다.

        결제는 어떤 방식으로 진행되나요?

        계좌이체로 진행하고, 지급일은 각 단계별 공정 완료 시점 기준으로 7일 이내 지급입니다.

        지체 상금은 어떻게 설정하시겠어요?

        계약 기간 초과 시 매일 계약금의 0.1%로 설정하고 싶습니다. 다만 천재지변이나 발주처 책임으로 인한 지연은 제외합니다.

        하자보수보증기간은요?

        준공일로부터 2년입니다. 하자 발생 시 통보받은 날로부터 7일 이내에 무상 보수 의무가 포함됩니다.

        혹시 분쟁 발생 시 해결 방법은요?

        서울중앙지방법원을 전속 관할로 명시하고자 합니다. 협의로 해결이 안 될 경우를 대비해서요.

        특약사항은 어떤 걸 넣고 싶으세요?

        자재 반입 일정은 발주처와 사전 협의하고, 외부 인력 사용 시 사전 동의 필요 등의 조항을 넣을 생각입니다.

        좋습니다. 그럼 도급인과 수급인 정보, 공사명, 기간, 금액, 의무사항까지 정리해서 도급계약서 초안 준비해보겠습니다.

        네, 계약일은 오늘 날짜로 기재하고, 서명 및 날인은 내일 현장에서 진행하죠.
    """

    contract_type = "도급"
    gpt_response = generate_contract(contract_type, test_conversation, call_gpt_api)
    
    try:
        data = json.loads(gpt_response)
        print("✅ JSON 파싱 성공")
    except json.JSONDecodeError as e:
        print("❌ JSON 파싱 실패:", str(e))
        
        
    print(json.dumps(data, ensure_ascii=False, indent=2))

