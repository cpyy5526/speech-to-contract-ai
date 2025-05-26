from contract_classifier import get_contract_type
from keyword_extractor import extract_fields
from contract_annotater import annotate_contract_text

import json
import openai
import os
from dotenv import load_dotenv, find_dotenv

#api key 보안
_=load_dotenv(find_dotenv())
openai.api_key = os.getenv("OPENAI_API_KEY")

# 임시 호출 함수/ 이후 메인 모듈의 gpt 호출 함수로 대체 되어야함
def call_gpt_api(prompt: list[dict]) -> str:
    return openai.chat.completions.create(model="gpt-4", messages = prompt, temperature = 0.2)

def main():
    # 1. 테스트용 구두 계약 대화 텍스트 (간단한 예시)
    conversation_text = """
    SPEAKER_00 : 면접 보셨던 박민지 씨 맞으시죠 ? 
    SPEAKER_01 : 연락 주셔서 감사합니다
    SPEAKER_00 : 이번에 저희가 개발팀 정규직으로 채용하려고 합니다 . 조건 확인차 다시 연락드렸어요.
    SPEAKER_01 : , 궁금했던 게 있어서요 . 근무 시간은 되나요 ? 
    SPEAKER_00 : 주 5일 오전 9시부터 6시까지고요 . 점심시간 1시간 포함입니다.
    SPEAKER_01 : , 예고는 자주 있나요 ? 
    SPEAKER_00 : 가끔 프로젝트 마감 시기엔 야근도 있어요 . 대신 초과 근무 수당은 따로 지급됩니다.
    SPEAKER_01 : 연봉은 정도로 책정되나요 ? 
    SPEAKER_00 : 경력 고려에서 연 4,200만 원 측정했고요 . 인센티브는 연 이후에 평가 기준 충족 시 지급돼요.
    SPEAKER_01 : , 복지나 휴가는 되나요 ? 
    SPEAKER_00 : 4대 보험은 당연히 가입되고요 . 연차는 입차 첫해 15일 , 점심식 돼 1일 1만 원 지원 , 명절 상여금도 있습니다.
    SPEAKER_01 : 계약 기간은 정규직이라고 하셨죠
    SPEAKER_00 : , 3개월 수습 후 정식 채용이고요 . 수습 기간 중에도 급여 100 % 지급입니다.
    SPEAKER_01 : 괜찮네요 . 입사는 언제부터 가능한가요 ? 
    SPEAKER_00 : 주 월요일이 가장 좋긴 , 더 필요하시면 조정 가능합니다.
    SPEAKER_01 : 월요일부터 가능합니다 . 그날 뵙겠습니다.
    SPEAKER_00 : 좋습니다 . 환영합니다 .
    """

    # 2. 계약 유형 추출
    contract_type = get_contract_type(conversation_text, call_gpt_api)
    print(f"\n[1] 계약 유형 추출 결과: {contract_type}")

    # 3. 키워드 추출
    contract_fields = extract_fields(conversation_text, contract_type, call_gpt_api)
    print(f"\n[2] 키워드 추출 결과 (JSON):\n{contract_fields}")
    
    annotations = annotate_contract_text(contract_type, contract_fields, call_gpt_api)
    print(f"\n[3] 누락 키워드에 대한 코멘트:\n{json.dumps(annotations, ensure_ascii=False, indent=2)}")
    
if __name__ == "__main__":
    main()