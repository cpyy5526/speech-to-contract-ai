import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import user_icon from './images/user_icon.png'
import "./Signup.css";

function Signup() {
  const navigate = useNavigate();
  const [form, setForm] = useState({
    username: "",
    password: "",
    name: "",
    email: "",
  });

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    alert("회원가입이 정상적으로 완료되었습니다!");
    navigate("/login"); // 회원가입 후 로그인 페이지로 이동
  };

  return (
    <div className="signup-wrapper">
      <div className="signup-box">
        <h2 className="title">회원가입</h2>

        <form className="signup-form" onSubmit={handleSubmit}>
          <label>아이디를 입력해주세요</label>
          <div className="input-box">
            <span><img src={user_icon} className="user_icon"></img></span>
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

          <label>이름을 입력해주세요</label>
          <div className="input-box">
            <span><img src={user_icon} className="user_icon"></img></span>
            <input
              type="text"
              name="name"
              placeholder="Name"
              value={form.name}
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
        </form>
      </div>
    </div>
  );
}

export default Signup;
