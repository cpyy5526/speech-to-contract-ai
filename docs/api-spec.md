## 공통 에러 응답

- 요청 실패 시 모든 API는 다음 형태의 응답으로 에러 메시지를 반환합니다.

```json
{
  "detail": "에러 설명 메시지"
}
```

## 1.  사용자 인증

<aside>

### [POST]  /auth/register

- 자체 회원가입
- 이메일, ID, 비밀번호 시스템에 저장
- **요청**
    - Content-Type: application/json
    - Request Body 예시
    
    ```json
    {
      "email": "user@example.com",
      "username": "user123",
      "password": "your_password"
    }
    ```
    
- **응답**
    - 성공: HTTP 204 No Content
    - 실패
    
    | **상황** | **HTTP Status** | **detail 메시지** |
    | --- | --- | --- |
    | 이메일 중복 | 409 Conflict | "Email already registered" |
    | 아이디 중복 | 409 Conflict | "Username already taken" |
    | 요청값 누락/
    형식 오류 | 400 Bad Request | "Missing or invalid fields" |
    | 비밀번호 형식 불일치 | 400 Bad Request | "Password does not meet security requirements" |
    | 서버 내부 오류 | 500 Internal Server Error | "Unexpected server error" |
</aside>

<aside>

### [POST]  /auth/login

- 자체 로그인
- ID/PW로 로그인하면 JWT 발급
- **요청**
    - Content-Type: application/json
    - Request Body 예시
    
    ```json
    {
      "username": "user123",
      "password": "your_password"
    }
    ```
    
- **응답**
    - 성공: HTTP 200 OK
    - 응답 데이터 예시
    
    ```json
    {
      "access_token": "jwt_access_token_here",
      "refresh_token": "jwt_refresh_token_here",
      "token_type": "bearer"
    }
    ```
    
    - 실패
    
    | **상황** | **HTTP Status** | **detail 메시지** |
    | --- | --- | --- |
    | 아이디 또는 비밀번호 오류 | 401 Unauthorized | "Invalid username or password" |
    | 요청값 누락/형식 오류 | 400 Bad Request | "Missing username or password" |
    | 서버 내부 오류 | 500 Internal Server Error | "Unexpected server error" |
</aside>

<aside>

### [POST]  /auth/verify-social

- 소셜 로그인 토큰 검증
- 자체 JWT 발급 및 서비스 접근 허용
- **요청**
    - Content-Type: application/json
    - Request Body 예시
    
    ```json
    {
      "provider": "google",
      "social_token": "social_login_token_here"
    }
    ```
    
- **응답 예시**
    - 성공: HTTP 200 OK
    - 응답 데이터 예시
    
    ```json
    {
      "access_token": "jwt_access_token_here",
      "refresh_token": "jwt_refresh_token_here",
      "token_type": "bearer"
    }
    ```
    
    - 실패
    
    | **상황** | **HTTP Status** | **detail 메시지** |
    | --- | --- | --- |
    | 지원하지 않는 provider | 400 Bad Request | "Unsupported provider" |
    | social_token 누락 | 400 Bad Request | "Missing social token" |
    | provider 누락 | 400 Bad Request | "Missing provider" |
    | 소셜 서버 검증 실패 | 401 Unauthorized | "Invalid social token" |
    | 소셜 서버 응답 오류 | 502 Bad Gateway | "Social server error" |
    | 서버 내부 오류 | 500 Internal Server Error | "Unexpected server error" |
</aside>

<aside>

### [POST]  /auth/token/refresh

- 클라이언트에서 Refresh Token을 보내면 새 Access Token 발급
- 다른 엔드포인트에서 Access Token이 만료되어 401 “Expired token”이 발생할 경우, 이 엔드포인트로 재발급받고 다시 요청해야 함
- **요청**
    - Content-Type: application/json
    - Request Body 예시
    
    ```json
    {
      "refresh_token": "refresh_token_here"
    }
    ```
    
- **응답 예시**
    - 성공: HTTP 200 OK
    - 응답 데이터 예시
    
    ```json
    {
      "access_token": "new_access_token_here",
      "token_type": "bearer"
    }
    ```
    
    - 실패
    
    | **상황** | **HTTP Status** | **detail 메시지** |
    | --- | --- | --- |
    | Refresh Token 누락 | 400 Bad Request | "Missing refresh token" |
    | 형식 오류 또는 인증 실패 | 401 Unauthorized | "Invalid token" |
    | Refresh Token 만료됨 | 401 Unauthorized | "Expired token" |
    | Refresh Token 폐기됨 | 403 Forbidden | "Revoked token" |
    | 서버 오류 | 500 Internal Server Error | "Unexpected server error" |
</aside>

<aside>

### [GET]  /user/me

- 현재 로그인한 사용자 정보 조회
- 페이지 새로고침 이후에도 로그인 상태를 인식하는 데 필요
- **요청**
    - Request Header
    
    ```json
    Authorization: Bearer <access_token>
    ```
    
- **응답**
    - 성공: HTTP 200 OK
    - 응답 데이터 예시
    
    ```json
    {
      "email": "user@example.com",
      "username": "user123"
    }
    ```
    
    - 실패
    
    | **상황** | **HTTP Status** | **detail 메시지** |
    | --- | --- | --- |
    | 토큰 누락 | 401 Unauthorized | “Missing token” |
    | 토큰 형식 오류 또는 검증 실패 | 401 Unauthorized | “Invalid token” |
    | 토큰 만료됨 | 401 Unauthorized | “Expired token” |
    | 서버 내부 오류 | 500 Internal Server Error | "Unexpected server error" |
</aside>

<aside>

### [POST]  /auth/password/forgot

- 비밀번호 찾기
- 이메일로 비밀번호 재설정 링크 전송
- **요청**
    - Content-Type: application/json
    - Request Body 예시
    
    ```json
    {
      "email": "user@example.com"
    }
    ```
    
- **응답**
    - 성공: HTTP 204 No Content
    - 실패
    
    | **상황** | **HTTP Status** | **detail 메시지** |
    | --- | --- | --- |
    | 이메일 포맷 오류 | 400 Bad Request | "Invalid email format" |
    | 요청값 누락 | 400 Bad Request | "Missing email" |
    | 서버 내부 오류 | 500 Internal Server Error | "Unexpected server error" |
</aside>

<aside>

### [POST]  /auth/password/reset

- 비밀번호 찾기로 전송된 재설정 링크를 통한 새 비밀번호 설정
- **요청**
    - Content-Type: application/json
    - Request Body 예시
    
    ```json
    {
      "token": "reset_token_here",
      "new_password": "new_password"
    }
    ```
    
- **응답 예시**
    - 성공: HTTP 204 No Content
    - 실패
    
    | **상황** | **HTTP Status** | **detail 메시지** |
    | --- | --- | --- |
    | 토큰 누락 | 400 Bad Request | "Missing token" |
    | 토큰 형식 오류, 만료, 검증 실패 | 401 Unauthorized | "Invalid or expired token" |
    | new_password 누락 | 400 Bad Request | "Missing new password" |
    | 비밀번호 형식 불일치 | 400 Bad Request | "Password does not meet security requirements" |
    | 서버 내부 오류 | 500 Internal Server Error | "Unexpected server error” |
</aside>

<aside>

### [POST]  /auth/password/change

- 로그인한 사용자의 비밀번호 변경
- **요청**
    - Request Header
    
    ```json
    Authorization: Bearer <access_token>
    ```
    
    - Content-Type: application/json
    - Request Body 예시
    
    ```json
    {
      "old_password": "current_password",
      "new_password": "new_password"
    }
    ```
    
- **응답**
    - 성공: HTTP 204 No Content
    - 실패
    
    | **상황** | **HTTP Status** | **detail 메시지** |
    | --- | --- | --- |
    | 토큰 누락 | 401 Unauthorized | “Missing token” |
    | 토큰 형식 오류 또는 검증 실패 | 401 Unauthorized | “Invalid token” |
    | 토큰 만료됨 | 401 Unauthorized | “Expired token” |
    | old_password 또는 new_password 누락 | 400 Bad Request | “Missing password fields” |
    | 비밀번호 형식 불일치 | 400 Bad Request | “Password does not meet security requirements” |
    | 인증 실패(기존 비밀번호 틀림) | 401 Unauthorized | “Invalid current password” |
    | 서버 내부 오류 | 500 Internal Server Error | "Unexpected server error" |
</aside>

<aside>

### [POST]  /auth/logout

- 서버: 요청한 사용자의 모든 토큰을 무효화하고 세션 종료
- 클라이언트: 요청 후 저장된 토큰을 삭제하고 로그인 화면으로 이동
- **요청**
    - Request Header
    
    ```json
    Authorization: Bearer <access_token>
    ```
    
- **응답**
    - 성공: HTTP 204 No Content
    - 실패
    
    | **상황** | **HTTP Status** | **detail 메시지** |
    | --- | --- | --- |
    | 토큰 누락 | 401 Unauthorized | “Missing token” |
    | 토큰 형식 오류 또는 검증 실패 | 401 Unauthorized | “Invalid token” |
    | 토큰 만료됨 | 401 Unauthorized | “Expired token” |
    | 서버 내부 오류 | 500 Internal Server Error | “Unexpected server error” |
</aside>

<aside>

### [DELETE]  /auth/delete-account

- 로그인한 사용자의 계정 삭제
- **요청**
    - Request Header
    
    ```json
    Authorization: Bearer <access_token>
    ```
    
- **응답**
    - 성공: HTTP 204 No Content
    - 실패
    
    | **상황** | **HTTP Status** | **detail 메시지** |
    | --- | --- | --- |
    | 토큰 누락 | 401 Unauthorized | “Missing token” |
    | 토큰 형식 오류 또는 검증 실패 | 401 Unauthorized | “Invalid token” |
    | 토큰 만료됨 | 401 Unauthorized | “Expired token” |
    | 사용자 정보 없음(DB 문제) | 500 Internal Server Error | “User not found” |
    | 서버 내부 오류 | 500 Internal Server Error | "Unexpected server error" |
</aside>

---

## 2.  음성 업로드 및 텍스트 변환

<aside>

### [POST]  /transcription/initiate

- 음성파일 업로드(+ 텍스트 변환) 예약 요청
- 실제 업로드는 반환된 upload_url로 별도 요청해야 함 (PUT /transcription/upload/{id})
- 서버에서는 업로드 요청을 수락했는지만 바로 응답
- 실제 파일 업로드 및 텍스트 변환은 백그라운드에서 계속 진행됨
    - Polling: 프론트엔드에서는 업로드 요청 후 GET /transcription/status를 수시로 요청하여 진행상황을 확인하고 완료 시 다음 단계(POST /contracts/generate) 진행
- **요청**
    - Request Header
    
    ```json
    Authorization: Bearer <access_token>
    ```
    
    - Content-Type: application/json
    - Request Body 예시
    
    ```json
    {
      "filename": "recording.wav"
    }
    ```
    
- **응답**
    - 성공: HTTP 202 Accepted
    - 응답 데이터 예시
    
    ```json
    {
      "upload_url": "https://upload.myservice.com/upload/audio/abc123-def456-uuid"
    }
    ```
    
    - 실패
    
    | **상황** | **HTTP Status** | **detail 메시지** |
    | --- | --- | --- |
    | 토큰 누락 | 401 Unauthorized | “Missing token” |
    | 토큰 형식 오류 또는 검증 실패 | 401 Unauthorized | “Invalid token” |
    | 토큰 만료됨 | 401 Unauthorized | “Expired token” |
    | 파일명 누락 | 400 Bad Request | “Missing file name” |
    | 허용되지 않는 파일 형식 | 415 Unsupported Media Type | “Unsupported audio format” |
    | 서버 내부 오류 | 500 Internal Server Error | "Unexpected server error" |
</aside>

<aside>

### [PUT]  /transcription/upload/{id}

- 음성 파일을 업로드를 위한 전용 엔드포인트
- **실제 호출 시 경로는 “/transcription/upload/{id}”가 아님**
    - 해당 경로는 API 명세를 위한 형식적인 제목. 실제 업로드 주소가 아님
    - **POST /transcription/initiate에서 반환된 upload_url로 요청해야 함**
- 내부적으로는 FastAPI 서버가 아닌 업로드 전용 서버(nginx)로의 요청
- **요청**
    - [PUT]  {upload_url}
        - 예: [PUT] https://upload.myservice.com/upload/audio/abc123-def456-uuid
    - **Content-Type: application/octet-stream**
    - Request Body: 업로드할 음성 파일의 바이너리 데이터
        - 파일 내용을 multipart/form-data로 감싸지 않고, 원시 데이터를 직접 포함
- **응답**
    - 성공: HTTP 204 No Content
    - 실패
    
    | **상황** | **HTTP Status** | **detail 메시지** |
    | --- | --- | --- |
    | 잘못된 upload_url 또는 만료 | 400 Bad Request | “Invalid or expired upload_url” |
    | 파일 용량 초과 | 413 Payload Too Large | “Audio file is too large” |
    | 허용되지 않는 형식 | 415 Unsupported Media Type | “Unsupported audio format” |
    | 서버 오류 | 500 Internal Server Error | “Unexpected server error” |
</aside>

<aside>

### [GET]  /transcription/status

- 현재 사용자의 녹음 파일 업로드 및 텍스트 변환 진행상황 조회
- 상태는 다음 7가지 중 하나
    1. “uploading”: 파일 업로드가 아직 진행 중
    2. “uploaded”: 파일이 백엔드 서버에 완전히 업로드됨
    3. “transcribing”: 서버 내부에서 음성을 텍스트로 변환 중
    4. “done”: 텍스트 변환까지 완료됨. 계약서 생성 프로세스 준비됨
    5. “upload_failed”: 파일 업로드 실패 (→ /transcription/initiate로 처음부터 재시도)
    6. “transcription_failed”: 음성 변환 실패 (→ /transcription/retry 또는 /transcription/cancel)
    7. “cancelled”: 사용자가 취소 요청하여 중단됨
- **요청**
    - Request Header
    
    ```json
    Authorization: Bearer <access_token>
    ```
    
- **응답**
    - 성공: HTTP 200 OK
    - 응답 데이터 예시
    
    ```json
    {
      "status": "transcribing"
    }
    ```
    
    - 실패
    
    | **상황** | **HTTP Status** | **detail 메시지** |
    | --- | --- | --- |
    | 토큰 누락 | 401 Unauthorized | “Missing token” |
    | 토큰 형식 오류 또는 검증 실패 | 401 Unauthorized | “Invalid token” |
    | 토큰 만료됨 | 401 Unauthorized | “Expired token” |
    | 업로드 요청 없음 또는 만료됨 | 404 Not Found | “No audio data for this user” |
    | 서버 내부 오류 | 500 Internal Server Error | "Unexpected server error" |
</aside>

<aside>

### [GET]  /transcription/retry

- 음성 파일 업로드 후 텍스트 변환에 실패한 경우, 업로드된 해당 파일을 대상으로 변환 재시도
- 상태(/transcription/status)가 “transcription_failed”인 경우만 가능
- **요청**
    - Request Header
    
    ```json
    Authorization: Bearer <access_token>
    ```
    
- **응답**
    - 성공: HTTP 202 Accepted
    - 응답 데이터 예시
    - 실패
    
    | **상황** | **HTTP Status** | **detail 메시지** |
    | --- | --- | --- |
    | 토큰 누락 | 401 Unauthorized | “Missing token” |
    | 토큰 형식 오류 또는 검증 실패 | 401 Unauthorized | “Invalid token” |
    | 토큰 만료됨 | 401 Unauthorized | “Expired token” |
    | 재시도 가능한 상태 아님 | 409 Conflict | “Cannot retry at this stage” |
    | 업로드 요청 없음 또는 만료됨 | 404 Not Found | “No audio data for this user” |
    | 서버 내부 오류 | 500 Internal Server Error | "Unexpected server error" |
</aside>

<aside>

### [POST]  /transcription/cancel

- 현재 사용자의 녹음 파일 업로드 또는 텍스트 변환을 중단 및 초기화
- 상태(/transcription/status)가 다음 4가지인 경우만 가능
    - “uploading”
    - “uploaded”
    - “transcribing”
    - “transcription_failed”
- **요청**
    - Request Header
    
    ```json
    Authorization: Bearer <access_token>
    ```
    
- **응답**
    - 성공: HTTP 204 No Content
    - 실패
    
    | **상황** | **HTTP Status** | **detail 메시지** |
    | --- | --- | --- |
    | 토큰 누락 | 401 Unauthorized | “Missing token” |
    | 토큰 형식 오류 또는 검증 실패 | 401 Unauthorized | “Invalid token” |
    | 토큰 만료됨 | 401 Unauthorized | “Expired token” |
    | 취소 가능한 상태 아님 | 409 Conflict | “Cannot cancel at this stage” |
    | 업로드 요청 없음 또는 이미 만료됨 | 404 Not Found | “No audio data for this user” |
    | 서버 내부 오류 | 500 Internal Server Error | "Unexpected server error" |
</aside>

---

## 3. 계약서 생성

<aside>

### [POST]  /contracts/generate

- 변환된 텍스트를 바탕으로 계약서 생성 시작
- Whisper 변환이 완료된 후에만(/audio/status → “done”) 요청 가능
- 실제 계약서 생성은 서버 내부에서 백그라운드로 수행되며, 상태는 별도 엔드포인트로 확인 가능
- 업로드 또는 변환 실패, 사용자 취소 시 호출하지 않음
- **요청**
    - Request Header
    
    ```json
    Authorization: Bearer <access_token>
    ```
    
- **응답**
    - 성공: HTTP 202 Accepted
    - 실패
    
    | **상황** | **HTTP Status** | **detail 메시지** |
    | --- | --- | --- |
    | 토큰 누락 | 401 Unauthorized | “Missing token” |
    | 토큰 형식 오류 또는 검증 실패 | 401 Unauthorized | “Invalid token” |
    | 토큰 만료됨 | 401 Unauthorized | “Expired token” |
    | 음성 업로드 또는 텍스트 변환 미완료/실패 | 409 Conflict | “Transcription not ready” |
    | 음성 업로드 요청 없음 또는 만료됨 | 404 Not Found | “No audio data for this user” |
    | 동일한 생성 작업이 이미 진행 중 | 409 Conflict | “Generation already in progress” |
    | 서버 내부 오류 | 500 Internal Server Error | "Unexpected server error" |
</aside>

<aside>

### [GET]  /contracts/generate/status

- 현재 사용자의 계약서 생성 진행상황 확인
- 상태는 다음 4가지 중 하나
    1. “generating”
    2. “done”
    3. “failed” (→ /contracts/generate로 재시도 또는 /contracts/generate/cancel)
    4. “cancelled”
- 생성 완료 시 contract_id 반환
- **요청**
    - Request Header
    
    ```json
    Authorization: Bearer <access_token>
    ```
    
- **응답**
    - 성공: HTTP 200 OK
    - 응답 데이터 예시
    
    ```json
    {
      "status": "generating"
    }
    ```
    
    ```json
    {
      "status": "done",
      "contract_id": "new_contract_id"
    }
    ```
    
    - 실패
    
    | **상황** | **HTTP Status** | **detail 메시지** |
    | --- | --- | --- |
    | 토큰 누락 | 401 Unauthorized | “Missing token” |
    | 토큰 형식 오류 또는 검증 실패 | 401 Unauthorized | “Invalid token” |
    | 토큰 만료됨 | 401 Unauthorized | “Expired token” |
    | 생성 요청 없음 또는 만료됨 | 404 Not Found | “No contract generation in progress” |
    | 서버 내부 오류 | 500 Internal Server Error | "Unexpected server error" |
</aside>

<aside>

### [POST]  /contracts/generate/cancel

- 계약서 생성 프로세스 중단
- 상태(/generate/status)가 “generating”, “failed”인 경우에만 가능
- **요청**
    - Request Header
    
    ```json
    Authorization: Bearer <access_token>
    ```
    
- **응답**
    - 성공: HTTP 204 No Content
    - 실패
    
    | **상황** | **HTTP Status** | **detail 메시지** |
    | --- | --- | --- |
    | 토큰 누락 | 401 Unauthorized | “Missing token” |
    | 토큰 형식 오류 또는 검증 실패 | 401 Unauthorized | “Invalid token” |
    | 토큰 만료됨 | 401 Unauthorized | “Expired token” |
    | 생성 요청이 없거나 만료됨 | 404 Not Found | “No contract generation in progress” |
    | 이미 완료되었거나 취소 불가능한 상태 | 409 Conflict | “Cannot cancel generation at this stage” |
    | 서버 내부 오류 | 500 Internal Server Error | "Unexpected server error" |
</aside>

---

## 4.  계약서 관리

<aside>

### [GET]  /contracts

- 사용자가 생성한 계약서 목록 조회
- 각 계약서는 생성일 기준으로 최신순 정렬됨
- **요청**
    - Request Header
    
    ```json
    Authorization: Bearer <access_token>
    ```
    
- **응답**
    - 성공: HTTP 200 OK
    - 응답 데이터 예시
    
    ```json
    [
      {
        "id": "contract_uuid_1",
        "contract_type": "고용",
        "generation_status": "done",
        "created_at": "2024-05-01T12:00:00Z",
        "updated_at": "2024-05-02T15:30:00Z"
      },
      {
        "id": "contract_uuid_2",
        "contract_type": "매매",
        "generation_status": "done",
        "created_at": "2024-04-25T09:10:00Z",
        "updated_at": "2024-04-25T09:20:00Z"
      }
    ]
    ```
    
    - 실패
    
    | **상황** | **HTTP Status** | **detail 메시지** |
    | --- | --- | --- |
    | 토큰 누락 | 401 Unauthorized | “Missing token” |
    | 토큰 형식 오류 또는 검증 실패 | 401 Unauthorized | “Invalid token” |
    | 토큰 만료됨 | 401 Unauthorized | “Expired token” |
    | DB 조회 실패 | 500 Internal Server Error | “Database query failed” |
    | 서버 내부 오류 | 500 Internal Server Error | “Unexpected server error” |
</aside>

<aside>

### [GET]  /contracts/{contract_id}

- 특정 계약서 내용 상세 조회 (JSON 데이터)
- **요청**
    - Request Header
    
    ```json
    Authorization: Bearer <access_token>
    ```
    
- **응답**
    - 성공: HTTP 200 OK
    - 계약서 데이터(contents)는 **계약서 규격화** 페이지의 정의된 형식을 따름
    - 응답 데이터 예시
    
    ```json
    {
      "contract_type": "고용",
      "contents": {
        "contract_type": "근로계약서",
        "employer": {
          "company_name": "ABC 주식회사",
          "representative_name": "홍길동"
        },
        "employee": {
          "name": "김영희",
          "resident_number": "900101-1234567"
        },
        ...
      },
      "created_at": "2024-05-01T12:00:00Z",
      "updated_at": "2024-05-02T15:30:00Z",
    }
    ```
    
    - 실패
    
    | **상황** | **HTTP Status** | **detail 메시지** |
    | --- | --- | --- |
    | 토큰 누락 | 401 Unauthorized | “Missing token” |
    | 토큰 형식 오류 또는 검증 실패 | 401 Unauthorized | “Invalid token” |
    | 토큰 만료됨 | 401 Unauthorized | “Expired token” |
    | 존재하지 않는 계약서 | 404 Not Found | “Contract not found” |
    | DB 조회 실패 | 500 Internal Server Error | “Database query failed” |
    | 서버 내부 오류 | 500 Internal Server Error | “Unexpected server error” |
</aside>

<aside>

### [PUT]  /contracts/{contract_id}

- 특정 계약서 내용 수정 및 저장
- 프론트엔드에서는 수정한 계약서 JSON 전송
- **요청**
    - Request Header
    
    ```json
    Authorization: Bearer <access_token>
    ```
    
    - Content-Type: application/json
    - Request Body 예시
    
    ```json
    {
      "contents": { ... }  // 수정된 전체 계약서 JSON
    }
    ```
    
- **응답**
    - 성공: HTTP 204 No Content
    - 실패
    
    | **상황** | **HTTP Status** | **detail 메시지** |
    | --- | --- | --- |
    | 토큰 누락 | 401 Unauthorized | “Missing token” |
    | 토큰 형식 오류 또는 검증 실패 | 401 Unauthorized | “Invalid token” |
    | 토큰 만료됨 | 401 Unauthorized | “Expired token” |
    | 대상 계약서가 존재하지 않음 | 404 Not Found | “Contract not found” |
    | 계약서 JSON 형식 오류 또는 필드 누락 | 400 Bad Request | “Missing or invalid contract fields” |
    | DB 저장 실패 | 500 Internal Server Error | “Database update failed” |
    | 서버 내부 오류 | 500 Internal Server Error | “Unexpected server error” |
</aside>

<aside>

### [GET]  /contracts/{contract_id}/suggestions

- 초기 계약서 생성 시의 빈 필드에 대한 GPT 제안 텍스트 조회
- 프론트엔드에서는 해당 필드가 비어 있고 제안이 존재하면 표시
- **요청**
    - Request Header
    
    ```json
    Authorization: Bearer <access_token>
    ```
    
- **응답**
    - 성공: HTTP 200 OK
    - Content-Type: application/json
    - 응답 데이터 예시
    
    ```json
    [
      {
        "field_path": "wage_details.wage_amount"
        "suggestion_text": "2025년 최저임금은 시간당 10,030원입니다"
      },
      ...
    ]
    ```
    
    - 실패
    
    | **상황** | **HTTP Status** | **detail 메시지** |
    | --- | --- | --- |
    | 토큰 누락 | 401 Unauthorized | "Missing token" |
    | 토큰 형식 오류 또는 검증 실패 | 401 Unauthorized | "Invalid token" |
    | 토큰 만료됨 | 401 Unauthorized | “Expired token” |
    | 대상 계약서가 존재하지 않음 | 404 Not Found | "Contract not found" |
    | DB 조회 실패 | 500 Internal Server Error | "Database query failed" |
    | 기타 서버 오류 | 500 Internal Server Error | "Unexpected server error" |
</aside>

<aside>

### [POST]  /contracts/{contract_id}/restore

- 최초 생성된 버전(initial_contents)으로 계약서 내용 되돌리기
- 최초 버전으로 덮어쓴 이후에는 되돌릴 수 없음
- **요청**
    - Request Header
    
    ```json
    Authorization: Bearer <access_token>
    ```
    
- **응답**
    - 성공: HTTP 204 No Content
    - 실패
    
    | **상황** | **HTTP Status** | **detail 메시지** |
    | --- | --- | --- |
    | 토큰 누락 | 401 Unauthorized | "Missing token" |
    | 토큰 형식 오류 또는 검증 실패 | 401 Unauthorized | "Invalid token" |
    | 토큰 만료됨 | 401 Unauthorized | “Expired token” |
    | 대상 계약서가 존재하지 않음 | 404 Not Found | "Contract not found" |
    | 초기 생성본 없음 | 500 Internal Server Error | "Initial contents missing" |
    | DB 저장 실패 | 500 Internal Server Error | "Database update failed" |
    | 기타 서버 오류 | 500 Internal Server Error | "Unexpected server error" |
</aside>

<aside>

### [DELETE]  /contracts/{contract_id}

- 특정 계약서 삭제
- **요청**
    - Request Header
    
    ```json
    Authorization: Bearer <access_token>
    ```
    
- **응답**
    - 성공: HTTP 204 No Content
    - 실패
    
    | **상황** | **HTTP Status** | **detail 메시지** |
    | --- | --- | --- |
    | 토큰 누락 | 401 Unauthorized | “Missing token” |
    | 토큰 형식 오류 또는 검증 실패 | 401 Unauthorized | “Invalid token” |
    | 토큰 만료됨 | 401 Unauthorized | “Expired token” |
    | 대상 계약서가 존재하지 않음 | 404 Not Found | “Contract not found” |
    | DB 삭제 실패 | 500 Internal Server Error | “Database update failed” |
    | 서버 내부 예외 | 500 Internal Server Error | “Unexpected server error” |
</aside>