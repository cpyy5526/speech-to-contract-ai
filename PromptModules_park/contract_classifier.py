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
    user_input: str,
    gpt_caller: Callable[[list[dict]], str]  # dict들의 리스트를 인자로 받아 문자열을 리턴하는 함수
) -> str:
    # 임시/ 이후 사용자의 음성파일이 텍스트로 변환된 값이 들어와야함
    user_input = """
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
        
    
    prompt = f"""
		다음 대화 내용을 읽고, 대화가 아래 계약 유형 중 하나에 해당하면 그 계약 유형만 정확히 한 단어로 출력하세요.  
		해당되지 않는다면 "기타"라고만 답하세요.  
		불필요한 설명 없이 결과만 출력해야 합니다.
		
		가능한 계약 유형:
		- 증여
		- 매매
		- 교환
		- 소비대차
		- 사용대차
		- 임대차
		- 고용
		- 도급
		- 여행계약
		- 위임
		- 임치
		- 조합
		- 종신정기금
		- 화해
		
		대화 내용:
		{user_input}
		"""
    messages = [{"role": "system", "content": "너는 계약서 작성 도우미야"},
                {"role": "user", "content": prompt}]
    response = gpt_caller(messages)
    result = response.choices[0].message.content.strip()

    # 보정: 결과가 예상 유형이 아닐 경우 '기타' 처리
    if result not in CONTRACT_TYPES:
        return "기타"

    return result

CONTRACT_TYPES = [
    "증여", "매매", "교환", "소비대차", "사용대차", "임대차",
    "고용", "도급", "여행계약", "위임", "임치", "조합",
    "종신정기금", "화해"
]






if __name__ == '__main__':
    print(classify_contract_type(input, call_gpt_api))