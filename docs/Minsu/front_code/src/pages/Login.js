import React, { useState } from "react";
import "../App.css";
import "../styles/Login.css";

import { useNavigate } from "react-router-dom";
import user_icon from '../images/user_icon.png';

import { login, loginWithGoogle } from "../services/authApiMock";
import { requestPasswordReset } from "../services/authApiMock";

import { useEffect, useRef } from "react";

function Login() {
  const navigate = useNavigate();
  const [showResetPanel, setShowResetPanel] = useState(false);
  const [resetEmail, setResetEmail] = useState("");
  const buttonRef = useRef();

  const [form, setForm] = useState({
    username: "",
    password: ""
  });

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleLogin = async () => {
    try {
      const data = await login(form.username, form.password);
      localStorage.setItem("access_token", data.access_token);
      localStorage.setItem("refresh_token", data.refresh_token);
      console.log(data.access_token, data.refresh_token);
      navigate("/home");
    } catch (err) {
      // 에러는 내부에서 처리됨
    }
  };

  const handleGoogleCredential = async (response) => {
    const idToken = response.credential;
    try {
      const data = await loginWithGoogle(idToken);
      localStorage.setItem("access_token", data.access_token);
      localStorage.setItem("refresh_token", data.refresh_token);
      navigate("/home");
    } catch (err) {
      console.error("❌ Google 로그인 실패:", err);
    }
  };

  useEffect(() => {
    if (window.google && buttonRef.current) {
      window.google.accounts.id.initialize({
        client_id: "675803498903-h1tjci01n2g6mmeea3vsqp3l4q74k64f.apps.googleusercontent.com",
        callback: handleGoogleCredential,
      });

      window.google.accounts.id.renderButton(buttonRef.current, {
        theme: "outline",
        size: "large",
        type: "standard",
      });

      window.google.accounts.id.prompt(); // 자동 로그인 시도
    }
  }, []);

  const handleResetRequest = async () => {
    try {
      await requestPasswordReset(resetEmail);
      alert("📬 이메일로 재설정 링크가 전송되었습니다.");
      setShowResetPanel(false);
    } catch (err) {
      // 에러는 내부에서 처리됨
    }
  };

  return (
    <div className="login-container">
      <div className="login-box">
        <h2 className="login-title">📝 계약서 생성 서비스</h2>

        <div className="input-group">
          <label>아이디</label>
          <div className="input-icon">
            <img src={user_icon} className="user_icon" alt="user" />
            <input
              type="text"
              name="username"
              placeholder="아이디를 입력하세요"
              value={form.username}
              onChange={handleChange}
              required
            />
          </div>
        </div>

        <div className="input-group">
          <label>비밀번호</label>
          <div className="input-icon">
            <span className="password_icon">🔒</span>
            <input
              type="password"
              name="password"
              placeholder="비밀번호를 입력하세요"
              value={form.password}
              onChange={handleChange}
              required
            />
          </div>
        </div>

        <p className="forgot-password" onClick={() => setShowResetPanel(true)}>
          비밀번호를 잊으셨나요?
        </p>

        <button className="btn login-btn" onClick={handleLogin}>
          로그인
        </button>

        <div ref={buttonRef} style={{ margin: "20px 0" }}></div>

        <button className="btn signup-btn" onClick={() => navigate("/signup")}>
          회원가입
        </button>
      </div>

      {showResetPanel && (
        <div className="modal-overlay">
          <div className="modal-content">
            <h3>🔑 비밀번호 재설정</h3>
            <p>가입한 이메일을 입력해 주세요</p>
            <input
              type="email"
              placeholder="example@email.com"
              value={resetEmail}
              onChange={(e) => setResetEmail(e.target.value)}
            />
            <div className="modal-buttons">
              <button className="btn" onClick={handleResetRequest}>
                링크 전송
              </button>
              <button className="btn" onClick={() => setShowResetPanel(false)}>
                닫기
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default Login;
