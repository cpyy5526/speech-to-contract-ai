from openai import OpenAI
from typing import Callable
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)


# 임시 호출 함수/ 이후 메인 모듈의 gpt 호출 함수로 대체 되어야함
def call_gpt_api(prompt):
    return client.chat.completions.create(model="gpt-4", messages = prompt, temperature = 0.2)

def classify_contract_type(
    conversation: str,
    gpt_caller: Callable[[list[dict]], str]  # dict들의 리스트를 인자로 받아 문자열을 리턴하는 함수
) -> str:       
    
    prompt = f"""
        당신은 대화 내용을 문석하여 계약 유형을 정확히 판단하는 법률 전문가 AI입니다. 

        ## 1단계: 대화 내용을 분석하여 핵심 사실을 정리하세요.
        - 누가 무엇을 제공합니까?
        - 상대방은 어떤 대가를 지급하거나 반환하기로 약정합니까?
        - 제공되는 것은 재산, 금전, 근로, 결과물 중 무엇입니까?
        - 거래가 무상인지 유상인지 구분하세요.

        ## 대화 내용:
        {conversation}

        ## 2단계: 위에서 정리한 사실을 바탕으로 법적 의미를 해석하세요.
        - 당사자들의 약정이 가져오는 법적 효과(소유권 이전, 사용권 부여, 근로 제공 등)를 명확히 합니다.
        - 당사자들이 기대하는 실질적 목적(소유, 이용, 보수 수취 등)을 파악합니다.

        ## 3단계: 아래 계약 유형 기준과 비교하여 가장 일치하는 유형을 선택하세요.
        - 증여: 무상으로 재산을 이전하는 계약.
        - 매매: 일방이 부동산의 소유권을 이전하고, 상대방이 그 대금을 지급하기로 약정하는 계약.
        - 교환: 쌍방이 서로 부동산의 소유권을 맞교환 하는 계약.
        - 소비대차: 일방이 금전 또는 대체물을 빌려주고, 상대방이 동일한 종류와 품질, 수량의 물건을 반환하기로 약정하는 계약.
        - 사용대차: 일방이 금전 외의 물건을 무상으로 빌려주고, 상대방이 사용·수익한 후 원물 그대로 반환하기로 약정하는 계약.
        - 임대차: 일방이 부동산을 유상으로 빌려주고, 상대방이 차임을 지급하며 사용·수익한 후 반환하기로 약정하는 계약.
        - 고용: 근로자와 사용자 간에 근로 제공 및 보수 지급 등 근로 조건을 정하는 계약. 
        - 도급: 일방이 건설공사를 완성할 것을 약정하고, 상대방이 이에 대한 보수를 지급하기로 하는 계약.

        ## 4단계: 최종 답변 출력
        - 반드시 위 유형 중 하나를 한 단어로만 출력하세요.
        - 해당하지 않으면 '기타'라고만 답하세요.
        - 그 외의 설명, 해석, 다른 표현은 절대 하지 마세요.

        👉 최종 답변 (한 단어로):
        """



    messages = [{"role": "system", "content": "당신은 계약서를 분석하는 법률 전문가 AI입니다."},
                {"role": "user", "content": prompt}]
    response = gpt_caller(messages)
    result = response.choices[0].message.content.strip()

    # 보정: 결과가 예상 유형이 아닐 경우 '기타' 처리
    if result not in CONTRACT_TYPES:
        return "기타"

    return result

CONTRACT_TYPES = [
    "증여", "매매", "교환", "소비대차", "사용대차", "임대차", "고용", "도급"
]



if __name__ == '__main__':
    test_conversation = """
        안녕하세요. 근로계약 관련해서 이야기 나누고 싶습니다.
        네, 언제부터 근무 가능한가요?
        다음 주 월요일부터 가능합니다.
        좋습니다. 주 5일, 하루 8시간 근무로 생각하고 있는데 괜찮으실까요?
        네, 괜찮습니다. 출근 시간은 몇 시인가요?
        오전 9시부터 오후 6시까지입니다. 점심시간은 1시간이고요.
        급여는 월 250만원으로 생각하고 있습니다. 세전 기준입니다.
        네, 확인했습니다. 4대 보험도 가입되나요?
        물론입니다. 입사와 동시에 4대 보험 가입 처리됩니다.
        계약 기간은 어떻게 되나요?
        처음 3개월은 수습 기간이고, 이후 정규직 전환입니다. 수습 기간에도 급여는 동일합니다.
        좋습니다. 계약서 작성은 언제 하면 될까요?
        오늘 바로 작성해도 괜찮을까요? 신분증만 지참해주시면 됩니다.
        네, 가져왔습니다. 서류 작성하겠습니다.
        감사합니다. 함께 일하게 되어 기대됩니다.
        """
        
    print(classify_contract_type(test_conversation, call_gpt_api))