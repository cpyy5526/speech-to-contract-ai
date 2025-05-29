// src/pages/ResetPassword.js
import React, { useState, useEffect } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { confirmPasswordReset } from "../services/authApiMock"; // 또는 authApi로 변경 가능

import "../styles/Reset_password.css";

function ResetPassword() {
  const [newPassword, setNewPassword] = useState("");
  const [token, setToken] = useState("");
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    const query = new URLSearchParams(location.search);
    const tokenParam = query.get("token");
    if (!tokenParam) {
          // 🔧 개발 중일 경우 테스트용 토큰 사용
        console.warn("개발용 테스트 토큰 사용 중");
        setToken("test_token"); // 또는 "expired" 등 테스트 케이스
        
        
        // 배포할때 사용할 코드
    //   alert("토큰이 없습니다. 이메일 링크를 다시 확인해주세요.");
    //   navigate("/login");
    } else {
      setToken(tokenParam);
    }
  }, [location.search, navigate]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const status = await confirmPasswordReset(token, newPassword);
      if (status === 204) {
        alert("비밀번호가 성공적으로 재설정되었습니다. 로그인 화면으로 이동합니다.");
        navigate("/login");
      }
    } catch (err) {
      // 에러 처리는 authApi에서 처리됨
    }
  };

  return (
    <div className="reset-password-container">
      <div className="reset-password-box">
        <h2>비밀번호 재설정</h2>
        <form onSubmit={handleSubmit}>
          <label>새 비밀번호</label>
          <input
            type="password"
            placeholder="New password"
            value={newPassword}
            onChange={(e) => setNewPassword(e.target.value)}
            required
          />
          <button type="submit">비밀번호 재설정</button>
        </form>
      </div>
    </div>
  );
}

export default ResetPassword;
