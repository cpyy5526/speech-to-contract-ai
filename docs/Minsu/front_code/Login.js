// src/Login.js
import React from "react";
import "./App.css";
import "./Login.css";


import { useNavigate } from "react-router-dom";
import { signInWithPopup } from "firebase/auth";
import { auth, provider } from "./firebase";
import google_icon from './images/google_icon.png';
import user_icon from './images/user_icon.png'

function Login() {
  const navigate = useNavigate();

  const handleGoogleLogin = async () => {
    try {
      await signInWithPopup(auth, provider);
      navigate("/home");
    } catch (err) {
      console.error("구글 로그인 실패:", err);
    }
  };

  return (
    <div className="login-container">
      <div className="login-box">
        <h2>로그인</h2>

        <div className="input-group">
          <label>아이디를 입력해주세요</label>
          <div className="input-icon">
            <span><img src={user_icon} className="user_icon"></img></span>
            <input type="text" placeholder="ID" />
          </div>
        </div>

        <div className="input-group">
          <label>비밀번호를 입력해주세요</label>
          <div className="input-icon">
            <span className="password_icon">🔒</span>
            <input type="password" placeholder="password" />
          </div>
        </div>

        <div className="find-password">
          <a href="#">비밀번호 찾기</a>
        </div>

        <button className="btn login-btn">로그인</button>

        <button className="btn google-btn" onClick={handleGoogleLogin}>
          <img src={google_icon} id="google_icon" />
          <span className="google-text">Google 계정으로 로그인</span>
        </button>

        <hr />
        <button className="btn signup-btn" onClick={()=>navigate("/signup")}>회원가입</button>
      </div>
    </div>
  );
}

export default Login;