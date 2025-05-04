# DB Schema

## Table Overview

```python
speech_to_contract_platform
│
├── auth_*
│   ├── users
│   └── user_tokens
│
└── contracts_*
    ├── contents
    ├── transcriptions
    └── gpt_suggestions
```

## auth_*

### users

- 사용자 기본 정보 관리

| **Column** | **Type** | **Description** |
| --- | --- | --- |
| id | UUID (PK) | Primary Key |
| email | TEXT (UNIQUE) | 이메일 주소 |
| username | TEXT (UNIQUE) | 사용자 ID |
| hashed_password | TEXT (nullable) | 자체 가입 사용자만 저장 |
| provider | TEXT (nullable) | 소셜 서비스 |
| provider_user_id | TEXT (nullable) | 소셜 서비스 사용자 ID |
| is_active | BOOLEAN | 탈퇴 여부 |
| created_at | TIMESTAMP | 가입 시각 |
| updated_at | TIMESTAMP | 마지막 로그인 시각 |

### user_tokens

| **Column** | **Type** | **Description** |
| --- | --- | --- |
| id | UUID (PK) | 고유 식별자 |
| user_id | UUID (FK) | 사용자 참조(auth_users.id, **ON DELETE CASCADE**) |
| token_type | TEXT | “access” / “refresh” |
| token | TEXT | JWT 또는 Refresh Token 본문 |
| is_revoked | BOOLEAN | 취소(폐기) 여부 |
| expires_at | TIMESTAMP | 만료 시각 |
| created_at | TIMESTAMP | 발급 시각 |
- 

## contracts_*

### main

- 계약서 데이터(JSON) 저장

| **Column** | **Type** | **Description** |
| --- | --- | --- |
| id | UUID (PK) | Primary Key |
| user_id | UUID (FK) | 생성한 사용자(auth_users.id, **ON DELETE CASCADE**) |
| contract_type | TEXT | 계약 유형 (예: “고용”, “매매” 등) |
| contents | JSONB | 계약서 전체 데이터 (JSON) |
| initial_contents | JSONB | 최초 생성된 버전 계약서 (복구용, 읽기 전용) |
| created_at | TIMESTAMP | 생성 시각 |
| updated_at | TIMESTAMP | 수정 시각 |
| generation_status | ENUM | “generating”, “done”, “failed”, “cancelled” |

### transcriptions

- 원본 음성 및 대화 텍스트 관리
    - 음성 및 대화 텍스트는 계약서 생성 후 자동으로 삭제
    - 대화 텍스트 서버에서 .txt 파일로 관리하고, DB에서는 파일명만 추적
        - 텍스트 분량이 상당히 긴 경우가 많아 텍스트 원본을 저장할 경우 부담이 큼
        - 장기 저장보다는 중간 가공에 사용되고 삭제될 일시적 데이터
        - 계약서 생성 로직에서는 파일 스트림 형태로 입출력
        

| **Column** | **Type** | **Description** |
| --- | --- | --- |
| id | UUID (PK) | Primary Key |
| user_id | UUID (FK) | 업로드한 사용자(auth_users.id, **ON DELETE CASCADE**) |
| status | ENUM | “uploading”, “uploaded”, “transcribing”, “done”, “upload_failed”, “transcription_failed”, “cancelled” |
| audio_file | TEXT | 업로드된 음성 파일 내부 식별자(UUID) |
| script_file | TEXT | 변환(및 전처리된) 대화 텍스트 파일 내부 식별자(UUID) |
| created_at | TIMESTAMP | 업로드 시각 |
| updated_at | TIMESTAMP | 상태 변경 시각 |

### gpt_suggestions

- 공란에 대한 GPT의 제안 텍스트 관리

| **Column** | **Type** | **Description** |
| --- | --- | --- |
| id | UUID (PK) | Primary Key |
| contract_id | UUID (FK) | 연결된 계약 ID (contracts_contents.id, **ON DELETE CASCADE**) |
| field_path | TEXT | 제안된 항목의 경로 (예: "wage_details.wage_amount") |
| suggestion_text | TEXT | GPT가 생성한 제안 문구 |
| created_at | TIMESTAMP | 제안 생성 시각 |