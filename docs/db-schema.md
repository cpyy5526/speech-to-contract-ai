# DB Schema

## Table Overview

```python
speech_to_contract_platform
│
├── auth_*
│   ├── users            // 사용자 정보
│   └── user_tokens      // JWT 토큰 관리
│
└── contracts_*
    ├── contents         // 계약서 JSON 데이터
    ├── transcriptions   // 업로드 음성 및 변환 텍스트 상태 관리
    └── gpt_suggestions  // 공란 필드에 대한 GPT 제안 텍스트
```

## auth_*

### users

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


## contracts_*

### contents

| **Column** | **Type** | **Description** |
| --- | --- | --- |
| id | UUID (PK) | Primary Key |
| user_id | UUID (FK) | 생성한 사용자(auth_users.id, **ON DELETE CASCADE**) |
| generation_id | UUID (FK, nullable) | 생성 추적용 FK (contracts_generations.id, **ON DELETE SET NULL**) |
| contract_type | TEXT | 계약 유형 (예: “고용”, “매매” 등) |
| contents | JSONB | 계약서 전체 데이터 (JSON) |
| initial_contents | JSONB | 최초 생성된 버전 계약서 (복구용, 읽기 전용) |
| created_at | TIMESTAMP | 생성 시각 |
| updated_at | TIMESTAMP | 수정 시각 |

### gpt_suggestions

| **Column** | **Type** | **Description** |
| --- | --- | --- |
| id | UUID (PK) | Primary Key |
| contract_id | UUID (FK) | 연결된 계약 ID (contracts_contents.id, **ON DELETE CASCADE**) |
| field_path | TEXT | 제안된 항목의 경로 (예: "wage_details.wage_amount") |
| suggestion_text | TEXT | GPT가 생성한 제안 문구 |
| created_at | TIMESTAMP | 제안 생성 시각 |

### transcriptions 

| **Column** | **Type** | **Description** |
| --- | --- | --- |
| id | UUID (PK) | Primary Key |
| user_id | UUID (FK) | 업로드한 사용자(auth_users.id, **ON DELETE CASCADE**) |
| status | ENUM | “uploading”, “uploaded”, “transcribing”, “done”, “upload_failed”, “transcription_failed”, “cancelled” |
| upload_url | TEXT(nullable) | 클라이언트에게 제공한 업로드 전용 URL |
| audio_file | TEXT | 업로드된 음성 파일 내부 식별자(UUID) |
| script_file | TEXT | 변환(및 전처리된) 대화 텍스트 파일 내부 식별자(UUID) |
| created_at | TIMESTAMP | 업로드 시각 |
| updated_at | TIMESTAMP | 상태 변경 시각 |

### generations

| **Column** | **Type** | **Description** |
| --- | --- | --- |
| id | UUID (PK) | Primary Key |
| user_id | UUID (FK) | 요청한 사용자(auth_users.id, **ON DELETE CASCADE**) |
| transcription_id | UUID (FK, nullable) | 참조한 음성 변환 데이터(contracts_transcriptions.id, **ON DELETE SET NULL**) |
| status | ENUM | “generating”, “done”, “failed”, “cancelled” |
| created_at | TIMESTAMP | 요청 시각 |
| updated_at | TIMESTAMP | 상태 변경 시각 |