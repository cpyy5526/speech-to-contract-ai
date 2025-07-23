// src/services/apiClient.js
import axios from "axios";

const api = axios.create({
  baseURL: "/api/", // 실제 서버 주소에 맞게 수정
  headers: {
    "Content-Type": "application/json",
  },
});

// 자동으로 토큰 붙이기
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("access_token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// 응답에서 access token 만료 처리
api.interceptors.response.use(
  (response) => response, // 성공 응답은 그대로 반환
  async (error) => {
    const originalRequest = error.config;

    // access token 만료시 재발급
    if (
      error.response &&
      error.response.status === 401 &&
      (
        error.response.data?.detail === "Expired token" ||
        error.response.data?.detail === "Missing token" ||
        error.response.data?.detail === "Invalid token" ||
        error.response.data?.detail === "Invalid or expired token"
      ) &&
      !originalRequest._retry
    ) {
      originalRequest._retry = true;

      const refreshToken = localStorage.getItem("refresh_token");
      if (!refreshToken) {
        alert("로그인 정보가 없습니다. 다시 로그인해주세요.");
        localStorage.clear();
        window.location.href = "/login";
        return Promise.reject(error);
      }

      try {
        const refreshResponse = await api.post("/auth/token/refresh", {
          refresh_token: refreshToken,
        });

        const newAccessToken = refreshResponse.data.access_token;
        localStorage.setItem("access_token", newAccessToken);

        // 재요청에 새로운 토큰 첨부
        originalRequest.headers = originalRequest.headers || {};
        originalRequest.headers.Authorization = `Bearer ${newAccessToken}`;

        return api(originalRequest); // 요청 재시도
      } catch (refreshError) {
        const msg = refreshError.response?.data?.detail;
        if (msg === "Revoked token") {
          alert("세션이 만료되었습니다. 다시 로그인해주세요.");
        } else if (msg === "Expired token") {
          alert("로그인 정보가 오래되었습니다. 다시 로그인해주세요.");
        } else if (msg === "Missing refresh token") {
          alert("로그인 정보가 없습니다. 다시 로그인해주세요.");
        } else if (msg === "Invalid token") {
          alert("로그인 인증에 실패하였습니다. 다시 로그인해주세요.");
        } else {
          alert("인증 오류가 발생했습니다. 다시 로그인해주세요.");
        }

        localStorage.clear();
        window.location.href = "/login";
        return Promise.reject(refreshError);
      }
    }

    // 여기서부터는 인증 관련 외 공통 에러 처리
    const status = error.response?.status;

    if (!status) {
      alert("🚫 서버 응답이 없습니다. 네트워크를 확인하거나 잠시 후 다시 시도해주세요.");
    }

    return Promise.reject(error); // 그 외 에러는 그대로 반환
  }
);


export default api;

