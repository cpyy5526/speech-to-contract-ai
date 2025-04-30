# 계약서 유형 타입 추출
import openai
import os
from dotenv import load_dotenv, find_dotenv
import json

#api key 보안
_=load_dotenv(find_dotenv())
openai.api_key = os.getenv("OPENAI_API_KEY")

# 사전 정의된 계약 유형 리스트
CONTRACT_TYPES = [
    "증여", "매매", "교환", "소비대차", "사용대차", "임대차",
    "고용", "도급", "여행계약", "위임", "임치", "조합",
    "종신정기금", "화해"
]

#계약 유형 추출
def get_contract_type(conversation_text: str)->str:
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
    response=openai.ChatCompletion.create(
        model="gpt-4",
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
        temperature=0.5,
        max_tokens=25
    )
    result_type= response["choices"][0]["message"]["content"].strip()
    
    # 보정: 결과가 예상 유형이 아닐 경우 '기타' 처리
    if result_type not in CONTRACT_TYPES:
        return "기타"

    return result_type

# 계약서 schema JSON 파일 불러오기
def load_schema(contract_type: str) -> dict:        
    base_dir = os.path.dirname(os.path.abspath(__file__))  # 현재 파일의 절대 경로 기준
    path = os.path.join(base_dir, "schemas", f"{contract_type}_schema.json")
    
    if not os.path.exists(path):
        raise FileNotFoundError(f"스키마 없음: {path}")
    
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
    
# 대화 내용에서 계약서 필드를 JSON 형식으로 추출하기
# by CoT
def extract_fields(conversation_text:str, contract_type:str)->dict:
    schema=load_schema(contract_type)
    
    keyword_matching_prompt=f"""
        당신은 구두 계약을 분석하여 하는 AI입니다.
        다음은 계약 유형: {contract_type}의 계약서 필드입니다.
        
        [스키마]
        {json.dumps(schema, indent=2, ensure_ascii=False)}
        
        [대화 내용]
        \"\"\"{conversation_text}\"\"\"

        위 대화에서 필요한 정보를 추출해 JSON 형식으로 출력하세요.
    """
    
    response=openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {
                "role":"system", 
                "content":keyword_matching_prompt
            },
        ],
        temperature=0.7,
        max_tokens=1024
    )
    
    content = response["choices"][0]["message"]["content"]
    json_start = content.find("{")
    try:
        return json.loads(content[json_start:])
    except json.JSONDecodeError:
        raise ValueError("GPT 응답에서 JSON 파싱 실패:\n" + content)