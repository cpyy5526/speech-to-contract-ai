// src/services/apiClient.js
import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8000/api", // 실제 서버 주소에 맞게 수정
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

    // access token 만료: 401 + detail === "Expired token"
    if (
      error.response &&
      error.response.status === 401 &&
      error.response.data?.detail === "Expired token" &&
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
        const refreshResponse = await axios.post("http://localhost:8000/auth/token/refresh", {
          refresh_token: refreshToken,
        });

        const newAccessToken = refreshResponse.data.access_token;
        localStorage.setItem("access_token", newAccessToken);

        // 재요청에 새로운 토큰 첨부
        originalRequest.headers.Authorization = `Bearer ${newAccessToken}`;
        return api(originalRequest); // 요청 재시도
      } catch (refreshError) {
        alert("토큰 갱신 실패. 다시 로그인해주세요.");
        localStorage.clear();
        window.location.href = "/login";
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error); // 그 외 에러는 그대로 반환
  }
);


export default api;

