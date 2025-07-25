import React, { useState, useRef, useEffect } from "react";
import "../styles/Home.css";
import micIcon from "../images/mic_icon.png";
import docIcon from "../images/doc_icon.png";
import { useNavigate } from "react-router-dom";
import { changePassword } from "../services/authApi"; // 또는 authApi로 교체 가능
import { deleteAccount } from "../services/authApi"; // 또는 authApi
import { logout } from "../services/authApi"; 
import { getContractList } from "../services/contractApi";
import { initiateTranscription } from "../services/convertApi";



function Home({ user }) {
  const navigate = useNavigate();
  const fileInputRef = useRef();
  const menuRef = useRef();
  const [contractList, setContractList] = useState([]);
  const [fileList, setFileList] = useState([]);



  const [showChangeModal, setShowChangeModal] = useState(false);
  const [oldPassword, setOldPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [menuOpen, setMenuOpen] = useState(false);
  
  const [sidebarOpen, setSidebarOpen] = useState(false);

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

  useEffect(() => {
  const fetchContractList = async () => {
    try {
      const result = await getContractList();
      setContractList(result);
    } catch (err) {
      console.error("계약서 목록 불러오기 실패:", err.response?.data?.detail || err.message);
    }
  };

  fetchContractList();
}, []);

  const handleLogout = async () => {
    try {
      const status = await logout();
      if (status === 204) {
        alert("로그아웃 되었습니다.");
        localStorage.clear();
        navigate("/login");
      }
    } catch (err) {
    }

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

  const handleFileChange = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    try {
      const uploadUrl = await initiateTranscription(file.name);  
      navigate("/converting", {
        state: {
          uploadUrl,
          audioBlob: file,
          filename: file.name,
        },
      });
    } catch (err) {
      console.error("업로드 URL 생성 실패:", err);
      alert("파일 업로드 준비 중 오류가 발생했습니다.");
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

  useEffect(() => {
    fetch("/contractForms/files.json")
      .then((res) => res.json())
      .then((data) => setFileList(data))
      .catch((err) => console.error("파일 목록 불러오기 실패:", err));
  }, []);
  

  const handleDownload = async (fileName) => {
    try {
      const response = await fetch(`/contractForms/${fileName}`);
      if (!response.ok) {
        throw new Error("파일 다운로드 실패");
      }
  
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
  
      const link = document.createElement("a");
      link.href = url;
      link.download = fileName;
      link.click();
  
      window.URL.revokeObjectURL(url); // 메모리 해제
    } catch (error) {
      alert("파일을 다운로드할 수 없습니다.");
      console.error("다운로드 오류:", error);
    }
  };


  return (
    <div className="home-container">
      <div className="mobile-header">
        <button className="hamburger" onClick={() => setSidebarOpen(true)}>☰</button>
        <div
          className="mobile-user"
          onClick={() => setMenuOpen(!menuOpen)}  // ✅ 추가
        >
          {user?.username}님
        </div>
      </div>
        {sidebarOpen && (
        <div className="mobile-sidebar-overlay" onClick={() => setSidebarOpen(false)}>
          <div className="mobile-sidebar" onClick={(e) => e.stopPropagation()}>
            <h3 className="sidebar-title">계약서 작성 목록</h3>
            <ul className="contract-list">
              {contractList.map((item) => (
                <li
                  key={item.id}
                  onClick={() => {
                    navigate(`/download?contract_id=${item.id}`);
                    setSidebarOpen(false); // 선택 시 닫기
                  }}
                >
                  <span>{item.created_at.slice(0, 10)}</span> {item.contract_type}
                </li>
              ))}
            </ul>
            <button onClick={() => setSidebarOpen(false)}>닫기</button>
          </div>
        </div>
        )}


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
          {contractList.map((item) => (
            <li
              key={item.id}
              onClick={() => navigate(`/download?contract_id=${item.id}`)}
              style={{ cursor: "pointer" }}
            >
              <span>{item.created_at.slice(0, 10)}</span> {item.contract_type}
            </li>
          ))}
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

        <hr style={{ margin: "40px 0", borderTop: "2px solid #ccc", width: "90%" }} />

        
          <h1 className="main-header">계약서 양식</h1>
          <div className="contract-grid">
            {fileList.map((fileName, idx) => (
              <button
                key={idx}
                className="custom-download-button"
                onClick={() => handleDownload(fileName)}
              >
                {fileName}
              </button>
            ))}
          </div>
              
      </main>

      {showChangeModal && (
        <div className="modal-overlay">
          <div className="modal-content">
            <h3 className="modal-title">🔐 비밀번호 변경</h3>
            <p className="modal-subtitle">현재 비밀번호와 새 비밀번호를 입력하세요</p>
            
            <input
              type="password"
              placeholder="현재 비밀번호"
              value={oldPassword}
              onChange={(e) => setOldPassword(e.target.value)}
              className="modal-input"
            />
            <input
              type="password"
              placeholder="새 비밀번호"
              value={newPassword}
              onChange={(e) => setNewPassword(e.target.value)}
              className="modal-input"
            />
            
            <div className="modal-buttons">
              <button className="btn primary" onClick={handlePasswordChange}>변경</button>
              <button className="btn cancel" onClick={() => setShowChangeModal(false)}>닫기</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default Home;