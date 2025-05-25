import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import user_icon from '../images/user_icon.png'
import "../styles/Signup.css";


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
      const response = await fetch("http://localhost:8000/auth/register", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email: form.email,
          username: form.username,
          password: form.password,
        }),
      });

      // 상태 코드에 따라 분기 처리
    if (response.status === 204) {
      navigate("/login");

    } 
    
    else if (response.status === 409) {
      const result = await response.json();

      if (result.detail === "Email already registered") {
        alert(" Email already registered.");
      }
       else if (result.detail === "Username already taken") {
        alert(" Username already taken.");
      } 
      else {
        alert(" Conflict: " + result.detail);
      }
    }

     else if (response.status === 400) {
      const result = await response.json();
      if (result.detail === "Missing or invalid fields") {
        alert(" Missing or invalid fields");
      } 
      else if (result.detail === "Password does not meet security requirements") {
        alert(" Password does not meet security requirements");
      } 
      else {
        alert(" Bad request: " + result.detail);
      }
    } 
    
    else if (response.status === 500) {
      alert(" Unexpected server error");
    } 

    else {
      const result = await response.json();
      alert(" 알 수 없는 오류: " + result.detail);
    }
  } 

  catch (error) {
    console.error("회원가입 요청 실패:", error);
    alert(" Failed to connect to the server. Please check your network.");
  }
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
