# 백엔드 프로젝트 디렉터리

```python
backend/
├── app/                        # 전체 서버 코드 폴더
│   ├── main.py                   # FastAPI 앱 실행 코드. 서버의 시작점
│   ├── __init__.py               # 패키지(app/) 인식용 파일
│   │
│   ├── core/                     # 서버 전반에서 사용하는 설정 및 공통 기능 모음
│   │   ├── llm.py                  # ChatGPT API 호출
│   │   ├── stt.py                  # STT API(OpenAI Whisper) 호출
│   │   ├── config.py               # 환경 변수 및 설정값 로드 (.env 파일 불러오기 등)
│   │   ├── security.py             # JWT 발급 및 검증, 비밀번호 암호화 관련 함수
│   │   ├── dependencies.py         # 공통으로 필요한 객체(DB 세션, 사용자 정보 등) 주입 함수
│   │   └── celery_app.py           # Celery 객체(비동기 작업 처리 큐) 초기화 설정
│   │
│   ├── db/                       # 데이터베이스 연결 설정
│   │   ├── session.py              # DB 세션 생성 (-> FastAPI에서 async로 DB 접근)
│   │   └── init_db.py              # 초기 테이블 생성 등 DB 초기화
│   │
│   ├── models/                   # 실제 DB 테이블과 연결되는 모델 정의 (SQLModel)
│   │   ├── user.py                 # auth_users 테이블
│   │   ├── token.py                # auth_user_tokens 테이블
│   │   ├── contract.py             # contracts_contents 테이블
│   │   ├── suggestion.py           # contracts_gpt_suggestions 테이블
│   │   ├── transcription.py        # contracts_transcriptions 테이블
│   │   └── generation.py           # contracts_generation 테이블
│   │
│   ├── prompts/                  # 계약서 생성 프롬프트 정의 및 GPT 응답 후처리
│   │   ├── preprocessor.py         # 입력 데이터 전처리
│   │   ├── stopwords.py            # 전처리에 사용될 한국어 불용어 목록 (자체 정의)
│   │   ├── type_classifier.py      # 계약 유형 판단
│   │   ├── keyword_extractor.py    # 키워드 추출 및 JSON 형태 계약서 생성
│   │   ├── annotater.py            # 공란 처리된 필드에 대한 정보 제안 생성
│   │   ├── keword_schema.py        # 계약 유형별 JSON 데이터 형식 정의
│   │   └── review_schema.py        # 공란 정보 제안 관련 출력 형식 정의
│   │
│   ├── schemas/                  # Pydantic 기반 API 입출력 데이터 형식 정의
│   │   ├── auth.py
│   │   ├── transcription.py
│   │   ├── generation.py
│   │   └── contract.py
│   │
│   ├── routers/                  # API 엔드포인트 함수
│   │   ├── auth.py                 # 로그인/회원가입 및 인증 관련 (/user/me 포함)
│   │   ├── transcriptions.py       # 음성 업로드 및 변환 관련
│   │   ├── generations.py          # 계약서 생성 관련
│   │   └── contracts.py            # 계약서 CRUD, 제안 텍스트 조회, 복원
│   │
│   ├── services/                 # 핵심 기능 함수 (비즈니스 로직)
│   │   ├── auth.py
│   │   ├── transcriptions.py
│   │   ├── generations.py
│   │   └── contracts.py
│   │
│   └── tasks/                    # Celery 기반 비동기 작업 정의
│       ├── transcriptions.py       # STT 호출 및 변환 관련 비동기 작업
│       └── generations.py          # GPT 호출 및 계약서 생성 관련 비동기 파이프라인
│
└── pyproject.toml                # 배포를 위한 프로젝트 설정 파일(빌드, 의존성, 툴 등)
```