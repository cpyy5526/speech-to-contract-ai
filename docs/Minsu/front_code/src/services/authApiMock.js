// src/services/authMock.js

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
