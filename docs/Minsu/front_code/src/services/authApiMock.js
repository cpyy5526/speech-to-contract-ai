// src/services/authMock.js
import api from "./apiClient";

// 일반 로그인 (Mock)
export async function login(username, password) {
  console.log("🔐 [Mock] 로그인 요청:", username, password);

  return new Promise((resolve, reject) => {
    setTimeout(() => {
      if (username === "test" && password === "1234") {
        console.log("✅ [Mock] 로그인 성공");
        resolve({
          access_token: "mock_access_token",
          refresh_token: "mock_refresh_token",
        });
      } else {
        console.warn("❌ [Mock] 로그인 실패");
        alert("로그인 실패");
        reject({
          response: {
            data: {
              status: 401,
              detail: "Invalid username or password",
            },
          },
        });
      }
    }, 1000);
  });
}

// 구글 로그인 (Mock)
export async function loginWithGoogle(idToken) {
  console.log("🔐 [Mock] 구글 로그인 요청:", idToken);

  return new Promise((resolve, reject) => {
    setTimeout(() => {
      if (idToken) {
        console.log("✅ [Mock] 구글 로그인 성공");
        resolve({
          access_token: "mock_google_access_token",
          refresh_token: "mock_google_refresh_token",
        });
      } else {
        reject({
          response: {
            data: {
              status: 400,
              detail: "Missing social token",
            },
          },
        });
      }
    }, 1000);
  });
}

// 현재 로그인된 사용자 정보 (Mock)
export async function getCurrentUser() {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({
        username: "mock_user",
        email: "mock@example.com",
      });
    }, 500);
  });
}


// 회원가입 요청  (Mock)
export async function signup({ email, username, password }) {
  console.log("📝 [Mock] 회원가입 요청:", email, username, password);

  return new Promise((resolve, reject) => {
    setTimeout(() => {
      if (username === "taken") {
        reject({
          response: {
            data: {
              status: 409,
              detail: "Username already taken",
            },
          },
        });
      } else if (email === "used@example.com") {
        reject({
          response: {
            data: {
              status: 409,
              detail: "Email already registered",
            },
          },
        });
      } else {
        console.log("✅ [Mock] 회원가입 성공");
        resolve(204); // 실제 서버는 204 반환
      }
    }, 1000);
  });
}


// 비밀번호 재설정 이메일 전송 요청 (Mock)
export async function requestPasswordReset(email) {
  console.log("📨 [Mock] 비밀번호 재설정 요청:", email);

  return new Promise((resolve, reject) => {
    setTimeout(() => {
      if (!email) {
        reject({
          response: {
            data: { status: 400, detail: "Missing email" },
          },
        });
      } else if (!email.includes("@")) {
        reject({
          response: {
            data: { status: 400, detail: "Invalid email format" },
          },
        });
      } else {
        console.log("✅ [Mock] 이메일 전송 완료 (204)");
        resolve(204); // 실제 서버와 동일하게 204 응답 시뮬레이션
      }
    }, 1000);
  });
}


// 비밀번호 재설정 요청 (Mock)
export async function confirmPasswordReset(token, newPassword) {
  console.log("🔐 [Mock] 비밀번호 재설정 요청:", token, newPassword);

  return new Promise((resolve, reject) => {
    setTimeout(() => {
      if (!token) {
        reject({
          response: {
            data: { status: 400, detail: "Missing token" },
          },
        });
      } else if (!newPassword) {
        reject({
          response: {
            data: { status: 400, detail: "Missing new password" },
          },
        });
      } else if (token === "expired") {
        reject({
          response: {
            data: { status: 401, detail: "Invalid or expired token" },
          },
        });
      } else if (newPassword.length < 8) {
        reject({
          response: {
            data: {
              status: 400,
              detail: "Password does not meet security requirements",
            },
          },
        });
      } else {
        console.log("✅ [Mock] 비밀번호 재설정 성공 (204)");
        resolve(204); // 실제 서버도 204 No Content 반환
      }
    }, 1000);
  });
}



// 비밀번호 변경 (로그인한 사용자) (Mock)
// src/services/authMock.js

export async function changePassword(oldPassword, newPassword) {
  console.log("🔐 [Mock] 비밀번호 변경 요청:", oldPassword, newPassword);

  return new Promise((resolve, reject) => {
    setTimeout(() => {
      // 1. 토큰 없거나 만료된 경우 시뮬레이션은 생략 (apiClient에서 처리되므로)

      // 2. 필드 누락
      if (!oldPassword || !newPassword) {
        reject({
          response: {
            data: {
              status: 400,
              detail: "Missing password fields",
            },
          },
        });
        return;
      }

      // 3. 비밀번호 보안 기준 불만족 (예: 2자 미만)
      if (newPassword.length < 2) {
        reject({
          response: {
            data: {
              status: 400,
              detail: "Password does not meet security requirements",
            },
          },
        });
        return;
      }

      // 4. 현재 비밀번호 불일치
      if (oldPassword !== "1234") {
        reject({
          response: {
            data: {
              status: 401,
              detail: "Invalid current password",
            },
          },
        });
        return;
      }

      // 5. 성공 시
      console.log("✅ [Mock] 비밀번호 변경 성공 (204)");
      resolve(204);
    }, 1000);
  });
}



// 로그인된 사용자 계정 삭제
export async function deleteAccount() {
  console.log("🗑️ [Mock] 계정 삭제 요청");

  return new Promise((resolve, reject) => {
    setTimeout(() => {
      const simulateError = false; // ← true로 바꾸면 실패 테스트 가능

      if (simulateError) {
        reject({
          response: {
            data: {
              status: 500,
              detail: "User not found", // 또는 "Unexpected server error"
            },
          },
        });
      } else {
        console.log("✅ [Mock] 계정 삭제 성공 (204)");
        resolve(204);
      }
    }, 1000);
  });
}
