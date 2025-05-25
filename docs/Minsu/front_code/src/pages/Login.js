import React, { useState } from "react";
import "../App.css";
import "../styles/Login.css";


import { useNavigate } from "react-router-dom";
import { signInWithPopup } from "firebase/auth";
import { auth, provider } from "../firebase";
import google_icon from '../images/google_icon.png';
import user_icon from '../images/user_icon.png'

import { login, loginWithGoogle } from "../services/authApiMock";

function Login() {
  const navigate = useNavigate();
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

        <p className="forgot-password" onClick={() => navigate("/reset")}>
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
    </div>
  );
}

export default Login;
