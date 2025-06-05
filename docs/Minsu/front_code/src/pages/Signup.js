import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import user_icon from '../images/user_icon.png'
import "../styles/Signup.css";
import { signup } from "../services/authApi"; // 또는 authApi



function Signup() {
  const navigate = useNavigate();
  const [form, setForm] = useState({
    username: "",
    password: "",
    email: "",
  });

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const status = await signup(form); // ✅ axios 기반 함수 호출
      if (status === 204) {
        alert("회원가입 성공! 로그인 페이지로 이동합니다.");
        navigate("/login");
      }
    } catch (err) {
      // 에러 처리는 authApi
    }
  };

  return (
    <div className="signup-wrapper">
      <div className="signup-box">
        <h2 className="title">회원가입</h2>

        <form className="signup-form" onSubmit={handleSubmit}>
          <label>아이디를 입력해주세요</label>
          <div className="input-box">
            <span><img src={user_icon} className="user_icon" alt="아이디 아이콘"></img></span>
            <input
              type="text"
              name="username"
              placeholder="ID"
              value={form.username}
              onChange={handleChange}
              required
            />
          </div>

          <label>비밀번호를 입력해주세요</label>
          <div className="input-box">
            <span>🔒</span>
            <input
              type="password"
              name="password"
              placeholder="Password"
              value={form.password}
              onChange={handleChange}
              required
            />
          </div>

          

          <label>이메일을 입력 해 주세요</label>
          <div className="input-box">
            <span>✉️</span>
            <input
              type="email"
              name="email"
              placeholder="E-mail"
              value={form.email}
              onChange={handleChange}
              required
            />
          </div>

          <hr />

          <button type="submit" className="submit-btn">
            회원가입
          </button>

          <button
            type="button"
            className="goto-login-btn"
            onClick={() => navigate("/login")}
          >
            이미 계정이 있으신가요? 로그인 하러 가기 →
          </button>
        </form>
      </div>
    </div>
  );
}

export default Signup;
