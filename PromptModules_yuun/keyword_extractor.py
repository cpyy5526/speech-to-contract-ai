# 계약서 키워드 추출 모듈

import openai
import os
import json
from typing import Callable
from dotenv import load_dotenv, find_dotenv

#api key 보안
_=load_dotenv(find_dotenv())
openai.api_key = os.getenv("OPENAI_API_KEY")

### 임시 호출 함수/ 배포 단계에서는 메인 모듈에 작성될테니 삭제해야함.
def call_gpt_api(prompt):
    return openai.ChatCompletion.create(model="gpt-4", message=prompt,temperature=0.2)

# 계약서 schema JSON 파일 불러오기
### -> 이후 DB schema에서 가져오는 것으로 변경해야 함함
def load_schema(contract_type: str) -> dict:        
    base_dir = os.path.dirname(os.path.abspath(__file__))  # 현재 파일의 절대 경로 기준
    path = os.path.join(base_dir, "schemas", f"{contract_type}_schema.json")
    
    if not os.path.exists(path):
        raise FileNotFoundError(f"스키마 없음: {path}")
    
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
    
# 대화 내용에서 계약서 필드를 JSON 형식으로 추출하기
# -> by CoT
def extract_fields(
    conversation_text:str,
    contract_type:str,
    gpt_caller:Callable[[list[dict]], str]
    )->dict:
    
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
    
    messages=[
            {
                "role":"system", 
                "content":keyword_matching_prompt
            },
        ],
    
    response=gpt_caller(messages)
    content = response["choices"][0]["message"]["content"]
    json_start = content.find("{")
    
    ### 추출 후 JSON 전달
    try:
        return json.loads(content[json_start:])
    except json.JSONDecodeError:
        raise ValueError("GPT 응답에서 JSON 파싱 실패:\n" + content)


