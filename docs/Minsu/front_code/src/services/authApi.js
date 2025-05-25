// src/services/authApi.js
import api from "./apiClient";

// 현재 로그인된 사용자 정보 가져오기
export async function getCurrentUser() {
  try {
    const response = await api.get("/user/me");
    return response.data; // 예: { username: "...", email: "..." }
  } catch (error) {
    const { status, detail } = error.response?.data || {};
    if (status === 401) {
      if (detail === "Missing token") {
        alert("로그인 정보가 없습니다. 다시 로그인해주세요.");
      } else if (detail === "Invalid token") {
        alert("유효하지 않은 토큰입니다. 다시 로그인해주세요.");
      } else if (detail === "Expired token") {
        alert("로그인 세션이 만료되었습니다.");
      }
    } else if (status === 500) {
      alert("서버 오류가 발생했습니다. 잠시 후 다시 시도해주세요.");
    } else {
      alert(`알 수 없는 오류: ${detail || "응답 없음"}`);
    }
    localStorage.clear();
    window.location.href = "/login";
    throw error;
  }
}



// 일반 로그인 요청
export async function login(username, password) {
  try {
    const response = await api.post("/auth/login", {
      username,
      password,
    });

    return response.data; // { access_token, refresh_token }
  } catch (error) {
    const { status, detail } = error.response?.data || {};

    switch (status) {
      case 400:
        alert("❗ 아이디 또는 비밀번호가 누락되었습니다.");
        break;
      case 401:
        alert("❌ 아이디 또는 비밀번호가 잘못되었습니다.");
        break;
      case 500:
        alert("⚠️ 서버 오류가 발생했습니다.");
        break;
      default:
        alert("❓ 알 수 없는 오류: " + (detail || "응답 없음"));
    }

    throw error;
  }
}

// 구글 로그인 요청
export async function loginWithGoogle(idToken) {
  try {
    const response = await api.post("/auth/verify-social", {
      provider: "google",
      social_token: idToken,
    });

    return response.data; // { access_token, refresh_token }
  } catch (error) {
    const { status, detail } = error.response?.data || {};

    if (status === 400) {
      alert("❗ 요청 오류: " + detail);
    } else if (status === 401) {
      alert("❌ 인증 실패: " + detail);
    } else if (status === 502) {
      alert("⚠️ 소셜 서버 오류");
    } else if (status === 500) {
      alert("⚠️ 서버 오류");
    } else {
      alert("❓ 알 수 없는 오류: " + (detail || "응답 없음"));
    }

    throw error;
  }
}


// 회원가입 요청
export async function signup({ email, username, password }) {
  try {
    const response = await api.post("/auth/register", {
      email,
      username,
      password,
    });

    return response.status; // 204 expected
  } catch (error) {
    const { status, detail } = error.response?.data || {};

    switch (status) {
      case 400:
        alert("❗ 필드 누락 또는 유효하지 않은 입력입니다.");
        break;
      case 409:
        if (detail === "Email already registered") {
          alert("❗ 이미 등록된 이메일입니다.");
        } else if (detail === "Username already taken") {
          alert("❗ 이미 사용 중인 아이디입니다.");
        } else {
          alert("❗ 충돌: " + detail);
        }
        break;
      case 500:
        alert("⚠️ 서버 오류가 발생했습니다.");
        break;
      default:
        alert("❓ 알 수 없는 오류: " + (detail || "응답 없음"));
    }

    throw error;
  }
}


// 비밀번호 재설정 이메일 전송 요청
export async function requestPasswordReset(email) {
  try {
    const response = await api.post("/auth/password/forgot", { email });
    return response.status; // 기대 응답: 204 No Content
  } catch (error) {
    const { status, detail } = error.response?.data || {};

    if (status === 400) {
      if (detail === "Invalid email format") {
        alert("❗ 잘못된 이메일 형식입니다.");
      } else if (detail === "Missing email") {
        alert("❗ 이메일이 입력되지 않았습니다.");
      } else {
        alert("❗ 요청 오류: " + detail);
      }
    } else if (status === 500) {
      alert("⚠️ 서버 오류가 발생했습니다. 잠시 후 다시 시도해주세요.");
    } else {
      alert("❓ 알 수 없는 오류: " + (detail || "응답 없음"));
    }

    throw error;
  }
}
