### AI PROMPT

import os
import openai
from typing import Callable
from dotenv import load_dotenv, find_dotenv

#api key 보안
_=load_dotenv(find_dotenv())
openai.api_key = os.getenv("OPENAI_API_KEY")

# 임시 호출 함수/ 배포 단계에서는 메인 모듈에 작성될테니 삭제해야함.
def call_gpt_api(prompt):
    return openai.ChatCompletion.create(model="gpt-4", message=prompt,temperature=0.2)

# 위의 AI 파트 예시 코드의 예시 함수
def process_input(
    user_input: str,
    gpt_caller: Callable[[list[dict]], str]  # dict들의 리스트를 인자로 받아 문자열을 리턴하는 함수
    ) -> str:
    
    user_input=""""""
    
    messages = [{"role": "system", "content": "너는 계약서 작성 도우미야"},
                {"role": "user", "content": user_input}]
    response = gpt_caller(messages)
    
    result = response['choices'][0]['message']['content'].strip()

    return result
    
# 테스트를 위한 로직 실행 함수
if __name__ == '__main__':    print(function(input, call_gpt_api))