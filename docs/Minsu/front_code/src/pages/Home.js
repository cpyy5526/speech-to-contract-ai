import React, { useState, useRef, useEffect } from "react";
import "../styles/Home.css";
import micIcon from "../images/mic_icon.png";
import docIcon from "../images/doc_icon.png";
import { auth, signOut } from "../firebase";
import { useNavigate } from "react-router-dom";
import { changePassword } from "../services/authApiMock"; // 또는 authApi로 교체 가능
import { deleteAccount } from "../services/authApiMock"; // 또는 authApi


function Home({ user }) {
  const navigate = useNavigate();
  const fileInputRef = useRef();
  const menuRef = useRef();

  const [showChangeModal, setShowChangeModal] = useState(false);
  const [oldPassword, setOldPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [menuOpen, setMenuOpen] = useState(false);

  useEffect(() => {
    const handleClickOutside = (e) => {
      if (menuRef.current && !menuRef.current.contains(e.target)) {
        setMenuOpen(false);
      }
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, []);

  const handleLogout = () => {
    localStorage.clear();
    window.location.href = "/login";
  };

  const handleDeleteAccount = async () => {
    if (!window.confirm("⚠️ 정말 계정을 삭제하시겠습니까? 이 작업은 되돌릴 수 없습니다.")) return;

    try {
      const status = await deleteAccount();
      if (status === 204) {
        alert("✅ 계정이 성공적으로 삭제되었습니다.");
        localStorage.clear();
        navigate("/login");
      }
    } catch (err) {
      console.error("계정 삭제 실패:", err);
    }
  };


  const handleUploadClick = () => {
    fileInputRef.current.click();
  };

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      console.log("선택된 파일:", file);
      alert("파일 업로드 완료: " + file.name);
    }
  };

  const handlePasswordChange = async () => {
    try {
      const status = await changePassword(oldPassword, newPassword);
      if (status === 204) {
        alert("비밀번호가 성공적으로 변경되었습니다. 다시 로그인해주세요.");
        localStorage.clear();
        navigate("/login");
      }
    } catch (err) {
      console.error("비밀번호 변경 실패:", err);
    }
  };

  return (
    <div className="home-container">
      <div className="user-info">
        {user && (
          <div className="user-menu-wrapper" ref={menuRef} style={{ position: "relative" }}>
            <span className="user-name" onClick={() => setMenuOpen(!menuOpen)} style={{ cursor: "pointer" }}>
              {user.username}님
            </span>
            {menuOpen && (
              <div className="user-menu" style={{
                position: "absolute",
                top: "100%",
                right: 0,
                background: "white",
                border: "1px solid #ccc",
                boxShadow: "0 2px 8px rgba(0, 0, 0, 0.15)",
                padding: "10px",
                borderRadius: "6px",
                zIndex: 1000,
                width: "100px",
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
              }}>
                <button style={{ width: "100%", textAlign: "center" }} onClick={() => setShowChangeModal(true)}>비밀번호 변경</button>
                <button style={{ width: "100%", textAlign: "center" }} onClick={handleLogout}>로그아웃</button>
                <button style={{ width: "100%", textAlign: "center" }} onClick={handleDeleteAccount}>계정 삭제</button>
              </div>
            )}
          </div>
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
            <img src={micIcon} onClick={() => navigate("/recording")} alt="Mic" />
            <img src={docIcon} onClick={handleUploadClick} alt="Doc" />
            <input
              type="file"
              accept="audio/*"
              ref={fileInputRef}
              onChange={handleFileChange}
              style={{ display: "none" }}
            />
          </div>
        </div>

        <div className="home-buttons">
          <button>사용방법</button>
          <button>계약서 예시</button>
        </div>
      </main>

      {showChangeModal && (
        <div className="modal-overlay">
          <div className="modal-content">
            <h3>비밀번호 변경</h3>
            <input
              type="password"
              placeholder="현재 비밀번호"
              value={oldPassword}
              onChange={(e) => setOldPassword(e.target.value)}
            />
            <input
              type="password"
              placeholder="새 비밀번호"
              value={newPassword}
              onChange={(e) => setNewPassword(e.target.value)}
            />
            <button onClick={handlePasswordChange}>변경</button>
            <button onClick={() => setShowChangeModal(false)}>닫기</button>
          </div>
        </div>
      )}
    </div>
  );
}

export default Home;