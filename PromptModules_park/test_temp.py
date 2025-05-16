# 설명하는 주석
## 테스트에 맞춰 수정해야하는 코드
### 배포단계 전에 수정해야하는 코드  

from openai import OpenAI 
from typing import Callable

### api_key를 파일 내부에 텍스트 형태로 작성하는 것은 보안상 문제가 될수 있음
### 따라서 배포단계에서는 api_key를 env 파일로 환경 변수로 설정하는 방식으로 변경해야함. 
client = OpenAI(api_key = "sk-...") 

### 임시 호출 함수/ 배포 단계에서는 메인 모듈에 작성될테니 삭제해야함.
def call_gpt_api(prompt):    
		return client.chat.completions.create(model="gpt-4", messages = prompt, temperature = 0.2)

## 프롬프트 함수, 어떤 프롬프트인지에 따라 "function"을 다른 함수명으로 정해주면 됨
## 예) 계약서 유형 판단 프롬프트: def classify_contract_type()
def function(
    user_input: str,    
    gpt_caller: Callable[[list[dict]], str]  # dict들의 리스트를 인자로 받아 문자열을 리턴하는 함수
    ) -> str:
    
    ### 임시 대화 내용 / 사용자의 음성파일이 텍스트로 변환된 값이 들어와야함    
    user_input = """      
    """
    
    ## 현재 함수에 맞는 프롬프트 작성 / ex) 계약서 유형을 판단하는 프롬프트, 계약서 유형에 따라 json을 생성하는 프롬프트
    # 프롬프트 내부에 사용자 대화 내용이 포함되어야하므로 user_input 있어야함.
    prompt = f"""
    대화 내용: {user_input} 
    """
    
    messages = [{"role": "system", "content": "너는 계약서 작성 도우미야"},                
                            {"role": "user", "content": prompt}]    
    
    response = gpt_caller(messages)

    # gpt 응답은 한번에 여러정보를 담고 있음. 그 중 모델이 생성한 텍스트만 추출하는 코드
    result = response.choices[0].message.content.strip()

    return result

## function을 위에서 정한 다른 함수명으로 변경
### 테스트용 main 함수 / 배포단계에서는 메인모듈에서 호출,실행 할테니 삭제하면 됨.
if __name__ == '__main__':    print(function(input, call_gpt_api))

