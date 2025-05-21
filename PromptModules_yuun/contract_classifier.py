# 계약서 유형 타입 추출 모듈

import openai
import os
from typing import Callable
from dotenv import load_dotenv, find_dotenv

#api key 보안
_=load_dotenv(find_dotenv())
openai.api_key = os.getenv("OPENAI_API_KEY")

### 임시 호출 함수/ 배포 단계에서는 메인 모듈에 작성될테니 삭제해야함.
def call_gpt_api(prompt):
    return openai.ChatCompletion.create(model="gpt-4", message=prompt,temperature=0.2)

# 사전 정의된 계약 유형 리스트
CONTRACT_TYPES = [
    "증여", "매매", "교환", "소비대차", "사용대차", "임대차",
    "고용", "도급", "여행계약", "위임", "임치", "조합",
    "종신정기금", "화해"
]

#계약 유형 추출
def get_contract_type(
    conversation_text: str,
    gpt_caller: Callable[[list[dict]], str]
    )->str:
    
    type_prompt=f"""
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
    """
    
    messages=[
            {
                "role":"system", 
                "content":type_prompt
            },
            {
                "role":"user",
                "content":f"다음은 고용계약을 위한 사용자 간 대화입니다. 대화 내용을 분석하여 적절한 계약 유형과 관련 키워드를 반환해주세요.:\n{conversation_text}"
            },
        ],
    
    response=gpt_caller(messages)

    result_type= response["choices"][0]["message"]["content"].strip()
    
    # 보정: 결과가 예상 유형이 아닐 경우 '기타' 처리
    if result_type not in CONTRACT_TYPES:
        return "기타"

    return result_type