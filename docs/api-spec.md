# API 명세

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
    
    | **상황** | **HTTP Status** | **detail 메시지 예시** |
    | --- | --- | --- |
    | 이메일 중복 | 409 Conflict | "Email already registered" |
    | 아이디 중복 | 409 Conflict | "Username already taken" |
    | 요청값 누락/
    형식 오류 | 400 Bad Request | "Missing or invalid fields" |
    | 비밀번호 형식 불일치 | 400 Bad Request | "Password does not meet security requirements" |
    | 서버 오류 | 500 Internal Server Error | "Internal server error" |
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
      "access_token": "jwt_token_here",
      "token_type": "bearer"
    }
    ```
    
    - 실패
    
    | **상황** | **HTTP Status** | **detail 메시지 예시** |
    | --- | --- | --- |
    | 아이디 또는 비밀번호 오류 | 401 Unauthorized | "Invalid username or password" |
    | 요청값 누락/형식 오류 | 400 Bad Request | "Missing username or password" |
    | 서버 오류 | 500 Internal Server Error | "Internal server error" |
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
      "access_token": "jwt_token_here",
      "token_type": "bearer"
    }
    ```
    
    - 실패
    
    | **상황** | **HTTP Status** | **detail 메시지 예시** |
    | --- | --- | --- |
    | 지원하지 않는 provider | 400 Bad Request | "Unsupported provider" |
    | social_token 누락 또는 비어있음 | 400 Bad Request | "Missing social token" |
    | provider 누락 또는 비어있음 | 400 Bad Request | "Missing provider" |
    | 소셜 서버 검증 실패 | 401 Unauthorized | "Invalid social token" |
    | 소셜 서버 응답 오류 | 502 Bad Gateway | "Social server error" |
    | 서버 내부 오류 | 500 Internal Server Error | "Internal server error" |
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
    
    | **상황** | **HTTP Status** | **detail 메시지 예시** |
    | --- | --- | --- |
    | Authorization 헤더 누락 | 401 Unauthorized | "Missing access token" |
    | 토큰 형식 오류 | 401 Unauthorized | "Invalid token format" |
    | 토큰 만료 | 401 Unauthorized | "Expired access token" |
    | 토큰 검증 실패(위조 등) | 401 Unauthorized | "Invalid access token" |
    | 서버 내부 오류 | 500 Internal Server Error | "Internal server error" |
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
    
    | **상황** | **HTTP Status** | **detail 메시지 예시** |
    | --- | --- | --- |
    | 이메일 포맷 오류 | 400 Bad Request | "Invalid email format" |
    | 요청값 누락 | 400 Bad Request | "Missing email" |
    | 서버 내부 오류 | 500 Internal Server Error | "Internal server error" |
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
    
    | **상황** | **HTTP Status** | **detail 메시지 예시** |
    | --- | --- | --- |
    | token 누락 | 400 Bad Request | "Missing token" |
    | token 형식 오류/만료/검증 실패 | 401 Unauthorized | "Invalid or expired token" |
    | new_password 누락 | 400 Bad Request | "Missing new password" |
    | 비밀번호 형식 불일치 | 400 Bad Request | "Password does not meet security requirements" |
    | 서버 내부 오류 | 500 Internal Server Error | "Internal server error" |
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
    
    | **상황** | **HTTP Status** | **detail 메시지 예시** |
    | --- | --- | --- |
    | old_password 또는 new_password 누락 | 400 Bad Request | "Missing password fields" |
    | 비밀번호 형식 불일치 | 400 Bad Request | "Password does not meet security requirements" |
    | 인증 실패(기존 비밀번호 틀림) | 401 Unauthorized | "Invalid current password" |
    | 서버 내부 오류 | 500 Internal Server Error | "Internal server error" |
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
    
    | **상황** | **HTTP Status** | **detail 메시지 예시** |
    | --- | --- | --- |
    | Authorization 헤더 누락 | 401 Unauthorized | "Missing access token" |
    | 토큰 형식 오류 | 401 Unauthorized | "Invalid token format" |
    | 토큰 만료 또는 검증 실패 | 401 Unauthorized | "Invalid or expired token" |
    | 사용자 정보 없음(DB 문제) | 500 Internal Server Error | "Internal server error" |
    | 서버 내부 오류 | 500 Internal Server Error | "Internal server error" |
</aside>

---

## 2.  계약서 생성

<aside>

### [POST]  /contracts/audio

- 현재 사용자의 녹음 파일을 서버에 업로드
- 파일 용량은 40MB로 제한 (일반적인 모바일 환경에서 30-35분 정도 용량)
- 서버에서는 업로드 요청을 수락했는지만 바로 응답
- 실제 파일 업로드는 백그라운드에서 계속 진행됨
    - Polling: 프론트엔드에서는 해당 엔드포인트 호출 후 아래 status 엔드포인트를 수시로 요청하여 진행상황을 확인하고 다음 단계(generate) 진행
- **요청**
    - Request Header
    
    ```json
    Authorization: Bearer <access_token>
    ```
    
    - Content-Type: multipart/form-data
    - Field name: audio_file
- **응답**
    - 성공: HTTP 202 Accepted
    - 실패
    
    | **상황** | **HTTP Status** | **detail 메시지 예시** |
    | --- | --- | --- |
    | 파일 누락 또는 필드 오류 | 400 Bad Request | “Missing or invalid audio file” |
    | 허용되지 않는 파일 형식 | 415 Unsupported Media Type | “Unsupported audio format” |
    | 파일 용량 초과 | 413 Payload Too Large | “Audio file is too large” |
    | 인증 실패 | 401 Unauthorized | “Missing or invalid access token” |
    | 서버 오류 | 500 Internal Server Error | “Internal server error” |
</aside>

<aside>

### [GET]  /contracts/audio/status

- 현재 사용자의 녹음 파일 업로드 및 텍스트 변환 진행상황 조회
- 상태는 다음 7가지 중 하나
    1. “uploading”: 파일 업로드가 아직 진행 중
    2. “uploaded”: 파일이 백엔드 서버에 완전히 업로드됨
    3. “transcribing”: 서버 내부에서 음성을 텍스트로 변환 중
    4. “done”: 텍스트 변환까지 완료됨. 계약서 생성 프로세스 준비됨
    5. “upload_failed”: 파일 업로드 실패
    6. “transcription_failed”: 음성 변환 실패
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
    
    | **상황** | **HTTP Status** | **detail 메시지 예시** |
    | --- | --- | --- |
    | 인증 실패 | 401 Unauthorized | “Missing or invalid access token” |
    | 업로드 요청 없음 또는 만료됨 | 404 Not Found | “No audio data for this user” |
    | 서버 오류 | 500 Internal Server Error | “Internal server error” |
</aside>

<aside>

### [POST]  /contracts/audio/cancel

- 현재 사용자의 녹음 파일 업로드 또는 텍스트 변환을 중단 및 초기화
- 상태(/audio/status)가 다음 3가지인 경우만 가능
    - “uploading”
    - “uploaded”
    - “transcribing”
- **요청**
    - Request Header
    
    ```json
    Authorization: Bearer <access_token>
    ```
    
- **응답**
    - 성공: HTTP 204 No Content
    - 실패
    
    | **상황** | **HTTP Status** | **detail 메시지 예시** |
    | --- | --- | --- |
    | 취소 가능한 상태가 아님 | 409 Conflict | “Cannot cancel at this stage” |
    | 업로드 요청 없음 또는 이미 만료됨 | 404 Not Found | “No audio data for this user” |
    | 인증 실패 | 401 Unauthorized | “Missing or invalid access token” |
    | 서버 오류 | 500 Internal Server Error | “Internal server error” |
</aside>

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
    
    | **상황** | **HTTP Status** | **detail 메시지 예시** |
    | --- | --- | --- |
    | 음성 업로드 또는 텍스트 변환 미완료/실패 | 409 Conflict | “Transcription not ready” |
    | 인증 실패 | 401 Unauthorized | “Missing or invalid access token” |
    | 음성 업로드 요청 없음 또는 만료됨 | 404 Not Found | “No audio data for this user” |
    | 서버 오류 | 500 Internal Server Error | “Internal server error” |
</aside>

<aside>

### [GET]  /contracts/generate/status

- 현재 사용자의 계약서 생성 진행상황 확인
- 상태는 다음 4가지 중 하나
    1. “generating”
    2. “done”
    3. “failed”
    4. “cancelled”
- 생성 완료 시 contract_id 반환
- 요청
    - Request Header
    
    ```json
    Authorization: Bearer <access_token>
    ```
    
- 응답
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
    
    | **상황** | **HTTP Status** | **detail 메시지 예시** |
    | --- | --- | --- |
    | 생성 요청 없음 또는 만료됨 | 404 Not Found | “No contract generation in progress” |
    | 인증 실패 | 401 Unauthorized | “Missing or invalid access token” |
    | 서버 오류 | 500 Internal Server Error | “Internal server error” |
</aside>

<aside>

### [POST]  /contracts/generate/cancel

- 계약서 생성 프로세스 중단
- 상태(/generate/status)가 “generating”인 경우만 가능
- **요청**
    - Request Header
    
    ```json
    Authorization: Bearer <access_token>
    ```
    
- **응답**
    - 성공: HTTP 204 No Content
    - 실패
    
    | **상황** | **HTTP Status** | **detail 메시지 예시** |
    | --- | --- | --- |
    | 생성 요청이 없거나 만료됨 | 404 Not Found | “No contract generation in progress” |
    | 이미 완료되었거나 취소 불가능한 상태 | 409 Conflict | “Cannot cancel generation at this stage” |
    | 인증 실패 | 401 Unauthorized | “Missing or invalid access token” |
    | 서버 오류 | 500 Internal Server Error | “Internal server error” |
</aside>

---

## 3.  계약서 관리

<aside>

### [GET]  /contracts

- 사용자가 생성한 계약서 목록 및 각각의 메타데이터 조회
- 요청
- 응답
</aside>

<aside>

### [GET]  /contracts/{contract_id}

- 저장된 특정 계약서 내용 상세 조회 (JSON 데이터)
- 요청
- 응답
</aside>

<aside>

### [PUT]  /contracts/{contract_id}

- 특정 계약서 내용 수정 및 저장
- 요청
- 응답
</aside>

<aside>

### [DELETE]  /contracts/{contract_id}

- 특정 계약서 삭제
- 요청
- 응답
</aside>

---