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

export default api;

