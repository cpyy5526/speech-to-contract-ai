import React, { useEffect, useState } from "react";
import { BrowserRouter as Router, Routes, Route, useNavigate, useLocation } from "react-router-dom";
import Login from "./Login";
import Signup from "./Signup";
import Home from "./Home";
import Recording from "./Recording";
import Converting from "./Converting";
import Download from "./Contract_download";
import { fetchWithAuth } from "./utils/FetchWithAuth";

//  로그인 확인 컴포넌트
function AppWithAuthCheck() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    const checkLogin = async () => {
      // 로그인 페이지에서는 검사 생략
      if (location.pathname === "/login" || location.pathname === "/signup") {
        setLoading(false);
        return;
      }

        try {
        const res = await fetchWithAuth("http://localhost:8000/user/me");

      if (res.status === 200) {
        const data = await res.json();
        setUser(data);
      } 
      else {
        const error = await res.json();
        
        if (res.status === 401 && error.detail === "Missing token") {
          alert("로그인 정보가 없습니다. 다시 로그인해주세요.");
        } 
        
        else if (res.status === 401 && error.detail === "Invalid token") {
          alert("유효하지 않은 토큰입니다. 다시 로그인해주세요.");
        } 
        
        else if (res.status === 500) {
          alert("서버 오류가 발생했습니다. 잠시 후 다시 시도해주세요.");
        } 
        
        else {
          alert("알 수 없는 오류: " + error.detail);
        }
        localStorage.clear();
        navigate("/login");
      }

    } 
    
      catch (err) {
      console.error("서버 연결 실패:", err);
      alert("서버에 연결할 수 없습니다. 인터넷 상태를 확인해주세요.");
      localStorage.clear();
      navigate("/login");
      }
  };

    checkLogin();
  }, [navigate, location.pathname]);

  if (loading) return <p>Loading...</p>;

  return (
    <Routes>
      <Route path="/" element={<Login />} />
      <Route path="/login" element={<Login />} />
      <Route path="/signup" element={<Signup />} />
      <Route path="/home" element={<Home user={user} />} />
      <Route path="/recording" element={<Recording user={user} />} />
      <Route path="/converting" element={<Converting user={user} />} />
      <Route path="/download" element={<Download user={user} />} />
    </Routes>
  );
}

function App() {
  useEffect(() => {
    const handleBeforeUnload = () => {
      if (window.streamsToClose) {
        window.streamsToClose.forEach((stream) => {
          stream.getTracks().forEach((track) => {
            console.log(" [App] 창 닫기/새로고침 시 마이크 종료:", track);
            track.stop();
          });
        });
      }
    };

    window.addEventListener("beforeunload", handleBeforeUnload);
    return () => window.removeEventListener("beforeunload", handleBeforeUnload);
  }, []);

  return (
    <Router>
      <AppWithAuthCheck />
    </Router>
  );
}

export default App;
