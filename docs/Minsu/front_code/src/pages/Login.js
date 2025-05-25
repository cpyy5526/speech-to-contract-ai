import React, { useState } from "react";
import "../App.css";
import "../styles/Login.css";
import { useNavigate } from "react-router-dom";
import { signInWithPopup } from "firebase/auth";
import { auth, provider } from "../firebase";
import google_icon from '../images/google_icon.png';
import user_icon from '../images/user_icon.png';


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
      const response = await fetch("http://localhost:8000/auth/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(form)
      });

      if (response.status === 200) {
        const data = await response.json();
        localStorage.setItem("access_token", data.access_token);
        localStorage.setItem("refresh_token", data.refresh_token);
        alert(" 로그인 성공!");
        navigate("/home");

      } 
      else if (response.status === 401) {
        alert(" Invalid username or password");
      } 
      
      else if (response.status === 400) {
        alert(" Missing username or password.");
      }
      
      else if (response.status === 500) {
        alert(" Unexpected server error.");
      }
      
      else {
        const result = await response.json();
        alert(" Unknown error: " + result.detail);
      }

    }
     catch (err) {
      console.error("Login request failed:", err);
      alert(" Failed to connect to the server. Please check your network.");
    }
  };

  const handleGoogleLogin = async () => {
     try {
      const result = await signInWithPopup(auth, provider);
      const idToken = await auth.currentUser.getIdToken();

      const response = await fetch("http://localhost:8000/auth/verify-social", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          provider: "google",
          social_token: idToken
        })
      });

      if (response.status === 200) {
        const data = await response.json();
        localStorage.setItem("access_token", data.access_token);
        localStorage.setItem("refresh_token", data.refresh_token);
        alert("Login successful!");
        navigate("/home");
      }

      else {
        const result = await response.json();

      if (response.status === 400) 
      {
        if (result.detail === "Unsupported provider") {
          alert("Unsupported provider.");
        } 
        
        else if (result.detail === "Missing social token") {
          alert("Missing social token.");
        }
        
        else if (result.detail === "Missing provider") {
          alert("Missing provider.");
        } 
        
        else {
          alert("Bad request: " + result.detail);
        }

      }
       else if (response.status === 401) 
        {
          if (result.detail === "Invalid social token") {
            alert("Invalid social token.");
          } 
          
          else 
          {
            alert("Unauthorized: " + result.detail);
          }
        } 
          
        else if (response.status === 502) 
          {
            alert("Social server error.");
          } 

          else if (response.status === 500) 
          {
            alert("Unexpected server error.");
          }

          else 
          {
            alert("Unknown error: " + result.detail);
          }
    }
     }
    catch (err) {
      console.error("Google login failed:", err);
      alert("Google login error.");
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
