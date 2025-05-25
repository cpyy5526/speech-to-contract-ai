import React, { useState } from "react";
import "../App.css";
import "../styles/Login.css";
import { useNavigate } from "react-router-dom";
import { signInWithPopup } from "firebase/auth";
import { auth, provider } from "../firebase";
import google_icon from '../images/google_icon.png';
import user_icon from '../images/user_icon.png';


import { login, loginWithGoogle } from "../services/authApiMock";
import { requestPasswordReset } from "../services/authApiMock";


function Login() {
  const navigate = useNavigate();
  const [showResetPanel, setShowResetPanel] = useState(false);
  const [resetEmail, setResetEmail] = useState("");



  const [form, setForm] = useState({
    username: "",
    password: ""
  });

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

 const handleLogin = async () => {
    try {
      const data = await login(form.username, form.password); // ✅ axios 방식 사용
      localStorage.setItem("access_token", data.access_token);
      localStorage.setItem("refresh_token", data.refresh_token);
      navigate("/home");
    } catch (err) {
      console.error("로그인 실패:", err);
      // 에러 처리는 authApi에서 처리됨
    }
  };

  const handleGoogleLogin = async () => {
    try {
      const result = await signInWithPopup(auth, provider);
      const idToken = await auth.currentUser.getIdToken();

      const data = await loginWithGoogle(idToken); // ✅ axios 방식 사용
      localStorage.setItem("access_token", data.access_token);
      localStorage.setItem("refresh_token", data.refresh_token);
      alert("Google 로그인 성공!");
      navigate("/home");
    } catch (err) {
      console.error("Google 로그인 실패:", err);
    }
  };

  
  const handleReset = async () => {
    try {
      const status = await requestPasswordReset(resetEmail);
      if (status === 204) {
        alert("📬 비밀번호 재설정 링크가 이메일로 전송되었습니다.");
      }
    } catch (err) {
      console.error("비밀번호 재설정 실패:", err);
      // 에러는 내부에서 alert 처리됨
    }
  };
  
  const handleResetRequest = async () => {
    try {
      await requestPasswordReset(resetEmail);
      alert("📬 이메일로 재설정 링크가 전송되었습니다.");
      setShowResetPanel(false);
    } catch (err) {
      console.error("비밀번호 재설정 실패:", err);
    }
  };


  return (
    <div className="login-container">
      <div className="login-box">
        <h2>로그인</h2>

        <div className="input-group">
          <label>아이디를 입력해주세요</label>
          <div className="input-icon">
            <span><img src={user_icon} className="user_icon" /></span>
            <input
              type="text"
              name="username"
              placeholder="ID"
              value={form.username}
              onChange={handleChange}
              required
            />
          </div>
        </div>

        <div className="input-group">
          <label>비밀번호를 입력해주세요</label>
          <div className="input-icon">
            <span className="password_icon">🔒</span>
            <input
              type="password"
              name="password"
              placeholder="password"
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

        <button className="btn google-btn" onClick={handleGoogleLogin}>
          <img src={google_icon} id="google_icon" />
          <span className="google-text">Google 계정으로 로그인</span>
        </button>

        <hr />
        <button className="btn signup-btn" onClick={() => navigate("/signup")}>회원가입</button>
      </div>

       {showResetPanel && (
        <div className="modal-overlay">
          <div className="modal-content">
            <h3>비밀번호 재설정</h3>
            <input
              type="email"
              placeholder="가입된 이메일을 입력하세요"
              value={resetEmail}
              onChange={(e) => setResetEmail(e.target.value)}
            />
            <div className="modal-buttons">
              <button onClick={handleResetRequest}>링크 전송</button>
              <button onClick={() => setShowResetPanel(false)}>닫기</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default Login;
