// src/services/authApi.js
import api from "./apiClient";

// 현재 로그인된 사용자 정보 가져오기
export async function getCurrentUser() {
  try {
    const response = await api.get("/user/me");
    return response.data; // 예: { username: "...", email: "..." }
  } catch (error) {
    const { status, detail } = error.response?.data || {};
    if (status === 500) {
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
        if (detail === "Missing username or password") {
          alert("❗ 아이디 또는 비밀번호가 누락되었습니다.");
        } else {
          alert("❗ 요청이 잘못되었습니다.");
        }
        break;

      case 401:
        if (detail === "Invalid username or password") {
          alert("❌ 아이디 또는 비밀번호가 잘못되었습니다.");
        } else {
          alert("❌ 인증 오류가 발생했습니다.");
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
      if (detail === "Unsupported provider") {
        alert("❗ 지원하지 않는 소셜 로그인입니다.");
      } else if (detail === "Missing social token") {
        alert("❗ 소셜 토큰이 누락되었습니다.");
      } else if (detail === "Missing provider") {
        alert("❗ provider 정보가 누락되었습니다.");
      } else {
        alert("❗ 요청 오류: " + detail);
      }
      
    } else if (status === 401) {
       if (detail === "Invalid social token") {
        alert("❌ 소셜 서버 인증에 실패했습니다. 다시 시도해주세요.");
      } else {
        alert("❌ 인증 오류: " + detail);
      }

    } else if (status === 502) {
      if (detail === "Social server error") {
        alert("⚠️ 소셜 서버로부터 응답이 없습니다. 잠시 후 다시 시도해주세요.");
      } else {
        alert("⚠️ 게이트웨이 오류: " + detail);
      }

    } else if (status === 500) {
      if (detail === "Unexpected server error") {
        alert("⚠️ 서버 내부 오류가 발생했습니다.");
      } else {
        alert("⚠️ 서버 오류: " + detail);
      }

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
        if (detail === "Missing or invalid fields") {
          alert("❗ 입력하지 않은 항목이 있거나 형식이 올바르지 않습니다. 다시 확인해주세요.");
        } else if (detail === "Password does not meet security requirements") {
          alert("❗ 비밀번호는 8~16자의 영문, 숫자, 특수문자를 포함해야 합니다.");
        } else {
          alert("❗ 오류: " + detail);
        }
        break;
      case 409:
        if (detail === "Email already registered") {
          alert("❗ 이미 등록된 이메일입니다.");
        } else if (detail === "Username already taken") {
          alert("❗ 이미 사용 중인 아이디입니다.");
        } else {
          alert("❗ 오류: " + detail);
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


// 비밀번호 재설정 요청
export async function confirmPasswordReset(token, newPassword) {
  try {
    const response = await api.post("/auth/password/reset", {
      token,
      new_password: newPassword,
    });

    return response.status; // 204 expected
  } catch (error) {
    const { status, detail } = error.response?.data || {};

    if (status === 400) {
      if (detail === "Missing token") {
        alert("❗ 토큰이 누락되었습니다.");
      } else if (detail === "Missing new password") {
        alert("❗ 새 비밀번호를 입력해주세요.");
      } else if (detail === "Password does not meet security requirements") {
        alert("❗ 비밀번호 보안 기준을 만족하지 않습니다.");
      } else {
        alert("❗ 잘못된 요청: " + detail);
      }
    } else if (status === 401) {
      alert("❌ 사용자 인증에 오류가 발생했습니다.");
    } else if (status === 500) {
      alert("⚠️ 서버 오류가 발생했습니다.");
    } else {
      alert("❓ 알 수 없는 오류: " + (detail || "응답 없음"));
    }

    throw error;
  }
}



// 비밀번호 변경 (로그인한 사용자)
export async function changePassword(oldPassword, newPassword) {
  try {
    const response = await api.post("/auth/password/change", {
      old_password: oldPassword,
      new_password: newPassword,
    });

    return response.status; // 204 expected
  } catch (error) {
    const { status, detail } = error.response?.data || {};

    if (status === 400) {
      if (detail === "Missing password fields") {
        alert("❗ 비밀번호 입력값이 누락되었습니다.");
      } else if (detail === "Password does not meet security requirements") {
        alert("❗ 새 비밀번호가 보안 기준에 부합하지 않습니다.");
      } else {
        alert("❗ 요청 오류: " + detail);
      }
    } else if (status === 401) {
      if (detail === "Invalid current password") {
        alert("❗ 현재 비밀번호가 잘못되었습니다.");
      }
    }else if (status === 500) {
      alert("⚠️ 서버 오류가 발생했습니다. 잠시 후 다시 시도해주세요.");
    } else {
      alert("❓ 알 수 없는 오류: " + (detail || "응답 없음"));
    }

    throw error;
  }
}


// 로그인된 사용자 계정 삭제
export async function deleteAccount() {
  try {
    const response = await api.delete("/auth/delete-account");
    return response.status; // 204 expected
  } catch (error) {
    const { status, detail } = error.response?.data || {};

    if (status === 401) {
      if (detail === "Missing token") {
        alert("❗ 인증 정보가 없습니다. 다시 로그인해주세요.");
      } else if (detail === "Invalid token") {
        alert("❗ 유효하지 않은 토큰입니다.");
      } else if (detail === "Expired token") {
        alert("❗ 세션이 만료되었습니다. 다시 로그인해주세요.");
      }
    } else if (status === 500) {
      if (detail === "User not found") {
        alert("❗ 사용자를 찾을 수 없습니다.");
      } else {
        alert("⚠️ 서버 오류가 발생했습니다.");
      }
    } else {
      alert("❓ 알 수 없는 오류: " + (detail || "응답 없음"));
    }

    throw error;
  }
}

