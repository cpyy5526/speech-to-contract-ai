# 내부 모듈의 GPT API 호출 규칙

## 의존성 주입 (Dependency Injection)

- 일반적으로 백엔드 개발에서는, 내부에서 호출하는 하위 함수 또는 모듈에서 외부 API 호출이 직접적으로 일어나도록 구성하지 않습니다.
- 백엔드 메인 모듈에서 ‘API를 호출하는 함수 또는 객체(인터페이스)’를 정의해 두고, 하위 모듈에서 이 ‘호출 객체(함수)’를 받아서 사용하는 방식으로 개발합니다. (의존성 주입)
- 의존성 주입 방식으로 코드를 구성해야 백엔드 서버의 메인 모듈에서 API 호출을 중심에서 제대로 통제할 수 있고, 로그 기록, 에러 처리, 보안 설계, 테스트 및 유지보수 등 전반적인 관리를 좀더 체계적으로 진행할 수 있습니다.
    - 하위 모듈 각각에서 직접적인 호출을 포함하게 되면, 구조가 일관적이지 못할 수밖에 없고, 호출 관리 및 예외 처리 등의 백엔드 메인 파트의 책임이 불필요하게 분산됩니다.
    - 즉, 우리 프로젝트의 경우에는 프롬프트 관련 모듈에서 GPT 호출이 일어나는 함수들에 일일이 그런 수정을 여러 번 거쳐야 할 수 있습니다.

## 호출 규칙

- Python에서는 ‘함수’ 역시 객체로 취급되므로, 기본적으로 하위 모듈에서는 다음과 같이 **GPT 호출 함수를 매개변수로 받도록** 함수를 작성하면 됩니다. (아래 코드에서는 gpt_caller)
- 매개변수로 받은 호출 함수에 (a, b, c)와 같이 함수에 맞게 인자를 붙여서 호출할 수 있습니다. (아래 코드에서는 gpt_caller(messages))

```python
# AI(프롬프트) 파트 예시 코드 (예: contract_prompt.py)
def process_input(
    user_input: str,
    gpt_caller: Callable[[list[dict]], str]  # dict들의 리스트를 인자로 받아 문자열을 리턴하는 함수
) -> str:
    messages = [{"role": "system", "content": "너는 계약서 작성 도우미야"},
                {"role": "user", "content": user_input}]
    response = gpt_caller(messages)
    response = response['choices'][0]['message']['content'].strip()
    ...
    return ...
```

- 실제 호출 함수는 백엔드 서버에서 다음과 같이 정의될 수 있습니다.

```python
# 백엔드 서버 예시 코드 (예: main.py)
import openai
import contract_prompt

# GPT API 호출 함수
async def call_gpt_api(prompt: list[dict]) -> str:
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages = prompt,
            temperature = 0.2
        )
        return response
    except Exception as e:
        '''
			      예외 처리
        '''
 
# 내부 API 정의 함수(하위 모듈 호출)
@app.post("/generate")
def generate_contract():
    try:
        ...
        result = contract_prompt.process_input(text, call_gpt_api)
        ...
    except Exception as e:
        ...
```

- 백엔드와 통합하기 전까지는 다음처럼 개발 중인 코드 내에서 **임시로 사용할 함수를 인자로 사용해서** 테스트하시면서 개발하시면 됩니다.

```python
# AI(프롬프트) 파트 예시 코드 (예: contract_prompt.py)

# 임시 호출 함수
def call_gpt_api(prompt):
    return openai.ChatCompletion.create(model="gpt-4", messages = prompt, temperature = 0.2)

# 위의 AI 파트 예시 코드의 예시 함수
def process_input(user_input, gpt_caller):
    ...
    
# 테스트를 위한 로직 실행 함수
def main():
    ...
    process_input(input, call_gpt_api)
    ...
    
main()
```