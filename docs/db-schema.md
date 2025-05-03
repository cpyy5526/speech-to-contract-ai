# DB Schema

## Table Overview

```python
speech_to_contract_platform
│
├── auth_*
│   ├── users
│   ├── social_accounts
│   └── user_tokens
│
└── contracts_*
    ├── contracts
    ├── transcriptions
    └── gpt_suggestions
```

## auth_*

## contracts_*

### contracts

- 계약서 데이터(JSON) 저장

| **Column** | **Type** | **Description** |
| --- | --- | --- |
| id | UUID (PK) | Primary Key |
| user_id | UUID (FK) | 생성한 사용자 |
| contract_type | TEXT | 계약 유형 (예: “고용”, “매매” 등) |
| contents | JSONB | 계약서 전체 데이터 (JSON) |
| created_at | TIMESTAMP | 생성일 |
| updated_at | TIMESTAMP | 수정일 |
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
| user_id | UUID (FK) | 업로드한 사용자 |
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
| contract_id | UUID (FK) | 연결된 계약 ID (contracts.id) |
| field_path | TEXT | 제안된 항목의 경로 (예: "wage_details.wage_amount") |
| suggestion_text | TEXT | GPT가 생성한 제안 문구 |
| created_at | TIMESTAMP | 제안 생성 시간 |