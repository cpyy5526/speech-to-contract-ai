import React from "react";
import "./Home.css";
import micIcon from "./images/mic_icon.png";
import docIcon from "./images/doc_icon.png";
import { auth, signOut } from "./firebase";
import { useNavigate } from "react-router-dom";

function Home() {
    const user = auth.currentUser;
    const navigate = useNavigate();

    const handleLogout = () => {
      signOut(auth)
        .then(() => {
          window.location.href = "/"; // 로그아웃 후 로그인 페이지로 이동
        })
        .catch((err) => console.error("로그아웃 실패:", err));
    };
    
  return (
    <div className="home-container">
          {/* 오른쪽 상단 사용자 정보 */}
      <div className="user-info">
        {user && (
          <>
            <img src={user.photoURL} alt="User" className="user-photo" />
            <span>{user.displayName}님</span>
            <button onClick={handleLogout}>로그아웃</button>
          </>
        )}
      </div>

      <aside className="sidebar">
        <h3 className="sidebar-title">계약서 작성 목록</h3>
        <ul className="contract-list">
          <li><span>2025-04-01</span> 문화계약서</li>
          <li><span>2025-03-27</span> 금융차용증서</li>
          <li><span>2025-03-25</span> 해외계약서</li>
          <li><span>2025-03-11</span> 부동산 임대차계약서</li>
        </ul>
      </aside>

      <main className="main-area">
        <header className="main-header">
          <h1>SMART CONTRACT</h1>
        </header>

        <div className="record-box">
          <p className="record-text">대화 내용의 녹음을 시작하거나 대화 내용 녹음 파일을 업로드해주세요</p>
          <div className="record-icons">
            <img src={micIcon} onClick={()=>navigate("/recording")} alt="Mic" />
            <img src={docIcon} alt="Doc" />
          </div>
        </div>

        <div className="home-buttons">
          <button>사용방법</button>
          <button>계약서 예시</button>
        </div>
      </main>
    </div>
  );
}

export default Home;
