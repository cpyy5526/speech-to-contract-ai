# 계약서 키워드 추출 

import os
import json
from jinja2 import Template
from contract_classifier import get_contract_type, extract_fields

# 계약서 템플릿 호출: /templates/{contract_type}_template.md
def load_template(contract_type: str) -> str:
    path = f"templates/{contract_type}_template.md"
    if not os.path.exists(path):
        raise FileNotFoundError(f"템플릿 없음: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def generate_contract(converation_text:str):
    # 1. 계약 유형 분류
    contract_type = get_contract_type(test_conversation)

    # 2. 계약 필드 추출
    contract_fields = extract_fields(test_conversation, contract_type)

    # 3. 템플릿 로딩
    # 이 부분은 빼야 됨
    try:
        template_str = load_template(contract_type)
    except FileNotFoundError as e:
        print(f"[X] {e}")
        exit(1)

    # 4. 템플릿 렌더링
    try:
        template = Template(template_str)
        rendered_contract = template.render(**contract_fields)
    except Exception as e:
        print(f"[X] 템플릿 렌더링 실패: {e}")
        exit(1)

    # 5. 출력
    print("\n" + "="*80 + "\n[계약서 마크다운 출력]\n" + "="*80 + "\n")
    print(rendered_contract)

# ✅ FastAPI 제거하고, 스크립트 실행 시 계약서 생성하도록 변경
if __name__ == "__main__":
    test_conversation = """
    A: 안녕하세요. 저는 XYZ마케팅 대표 이지은입니다. 마케팅 프로젝트가 많아져서 계약직으로 한 분을 모시고 싶어요.

    B: 안녕하세요. 저는 김지훈이고요. 어떤 업무를 맡게 될까요?

    A: 주로 SNS 콘텐츠 기획과 광고 분석 업무예요. 경력자 우대이고, 계약 기간은 6개월입니다.

    B: 네, 괜찮습니다. 근무 시간은 어떻게 되나요?

    A: 오전 9시부터 오후 6시까지, 월요일부터 금요일까지예요. 중간에 점심시간 한 시간 포함이고요.

    B: 급여는 어떻게 되나요?

    A: 월 320만 원이고, 매월 25일에 계좌로 입금됩니다.

    B: 4대 보험은 다 가입되나요?

    A: 네. 국민연금, 건강보험, 고용보험, 산재보험 모두 가입해드려요.

    B: 알겠습니다. 계약서는 준비되었나요?

    A: 네, 오늘 안으로 이메일로 보내드릴게요. 계약 시작일은 다음 주 월요일인 5월 6일부터고, 종료일은 11월 5일까지예요.

    B: 좋습니다. 제 인적 사항도 보내드릴게요.

    A: 네. 이름, 주소, 연락처, 주민등록번호 보내주시면 바로 작성하겠습니다.
    """

    generate_contract(test_conversation)
