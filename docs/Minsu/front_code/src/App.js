import React, { useEffect, useState } from "react";
import { BrowserRouter as Router, Routes, Route, useNavigate, useLocation } from "react-router-dom";
import Login from "./pages/Login";
import Signup from "./pages/Signup";
import Home from "./pages/Home";
import Recording from "./pages/Recording";
import Converting from "./pages/Converting";
import Download from "./pages/Contract_download";
import { getCurrentUser } from "./services/authApiMock"; 

//  로그인 확인 컴포넌트
function AppWithAuthCheck() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();
  const location = useLocation();


  useEffect(() => {
    const checkLogin = async () => {
      if (location.pathname === "/login" || location.pathname === "/signup") {
        setLoading(false);
        return;
      }

      try {
        const userData = await getCurrentUser(); // ✅ Axios 사용
        setUser(userData);
      } catch (err) {
        console.error("로그인 체크 실패:", err);
        // 이미 authApi에서 처리함
      } finally {
        setLoading(false);
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

