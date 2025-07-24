import React, { useEffect, useRef, useState, useCallback } from "react";
import "../styles/Contract_download.css";
import jsPDF from "jspdf";
import html2canvas from "html2canvas";
import { useLocation } from "react-router-dom";
import { useNavigate } from "react-router-dom";
import {
  getContractContent,
  getContractList,
  updateContractContent,
  getSuggestions,
  restoreContract,
  deleteContract
} from "../services/contractApi";

import GiftContract from "../Contract_types/GiftContract/GiftContract";
import ConstructionContract from "../Contract_types/ConstructionContract/ConstructionContract";
import EmploymentContract from "../Contract_types/EmploymentContract/EmploymentContract";
import ExchangeContract from "../Contract_types/ExchangeContract/ExchangeContract";
import LeaseContract from "../Contract_types/LeaseContract/LeaseContract";
import LoanContract from "../Contract_types/LoanContract/LoanContract";
import SaleContract from "../Contract_types/SaleContract/SaleContract";
import UsageLoanContract from "../Contract_types/UsageLoanContract/UsageLoanContract";



function Contract_download() {
  const [contract, setContract] = useState(null);
  const [contractList, setContractList] = useState([]);
  const [suggestions, setSuggestions] = useState([]);
  const [sidebarVisible, setSidebarVisible] = useState(true);


  const contractRef = useRef();
  const contractComponentRef  = useRef();
  const location = useLocation();

  const params = new URLSearchParams(location.search);
  const contractId = params.get("contract_id");

  const navigate = useNavigate();
  const toggleSidebar = () => {
    setSidebarVisible((prev) => !prev);
  };

  

  useEffect(() => {
    const fetchContracts = async () => {
      try {
        const result = await getContractList();
        setContractList(result);
 
      } catch (err) {
        console.error("계약서 목록 불러오기 실패:", err.response?.data?.detail || err.message);
      }
    };

    fetchContracts();
  }, []);

  const fetchContract = useCallback(async () => {
    try {
      const result = await getContractContent(contractId);
      setContract(result);
      
      const suggestionResult = await getSuggestions(contractId);
      setSuggestions(suggestionResult);
    } catch (err) {
      console.error("계약서 불러오기 실패:", err.response?.data?.detail || err.message);
    }
  }, [contractId]);
  
  useEffect(() => {
      if (contractId) fetchContract();
  }, [contractId, fetchContract]);

  const handleSave = async () => {
    try {
    const edited = contractComponentRef.current.extract();
      await updateContractContent(contractId, edited);
      window.location.reload();
    } catch (err) {
      console.error("❌ 저장 실패:", err);
    }
  };



  const handleDownload = async () => {
    const pages = document.querySelectorAll(".page");
    const pdf = new jsPDF("p", "mm", "a4");

    for (let i = 0; i < pages.length; i++) {
      const canvas = await html2canvas(pages[i], {
        scale: 2, // 🔍 고해상도 렌더링
      });
      const imgData = canvas.toDataURL("image/png");

      const imgWidth = 210;
      const imgHeight = (canvas.height * imgWidth) / canvas.width;

      if (i > 0) pdf.addPage();
      pdf.addImage(imgData, "PNG", 0, 0, imgWidth, imgHeight);
    }

    pdf.save(`${contract.contract_type || "계약서"}.pdf`);
  };







  const handleRestore = async () => {
    if (!window.confirm("⚠️ 초기 생성 상태로 되돌리시겠습니까? 변경된 내용은 모두 사라집니다.")) return;

    try {
      await restoreContract(contractId);
      alert("복구 완료");
      fetchContract();
    } catch (err) {
      console.error("❌ 복구 실패:", err.response?.data?.detail || err.message);
    }
  };

  const handleDelete = async () => {
    if (!window.confirm("🗑️ 정말 이 계약서를 삭제하시겠습니까? 삭제 후 되돌릴 수 없습니다.")) return;

    try {
      await deleteContract(contractId);
      alert("✅ 계약서가 삭제되었습니다.");
      setContractList((prevList) => prevList.filter(item => item.id !== contractId));
      setContract(null);
      navigate("/download");
    } catch (err) {
      console.error("❌ 삭제 실패:", err.response?.data?.detail || err.message);
    }
  };



  return (
    <div className="download-container">
      {/* 📌 사이드바 표시 여부 */}
      {sidebarVisible && (
        <aside className="sidebar">
          <button onClick={() => navigate("/home")} className="go-home-btn">⬅ 메인페이지</button>
          <h3 className="sidebar-title">계약서 작성 목록</h3>
          <ul className="contract-list">
            {contractList.map((item) => (
              <li
                key={item.id}
                className={item.id === contractId ? "active" : ""}
                onClick={() => navigate(`/download?contract_id=${item.id}`)}
              >
                <span>{item.created_at.slice(0, 10)}</span> {item.contract_type}
              </li>
            ))}
          </ul>
        </aside>
      )}

      <main className={`preview-area ${sidebarVisible ? "" : "expanded"}`}>
        {/* 햄버거 메뉴 버튼 */}
        <button className="toggle-sidebar-btn" onClick={toggleSidebar}>
          ☰
        </button>
        <div  ref={contractRef}>
          {!contract ? (
            <p>계약서를 선택해주세요</p>
              ) : contract.contract_type === "증여" ? (
                <GiftContract ref={contractComponentRef } contract={contract} suggestions={suggestions} />
              ) : contract.contract_type === "도급" ? (
                <ConstructionContract ref={contractComponentRef } contract={contract} suggestions={suggestions} />
              ) : contract.contract_type === "고용" ? (
                <EmploymentContract ref={contractComponentRef } contract={contract.contents} suggestions={suggestions} />
              ) : contract.contract_type === "교환" ? (
                <ExchangeContract ref={contractComponentRef } contract={contract} suggestions={suggestions} />
              ) : contract.contract_type === "임대차" ? (
                <LeaseContract ref={contractComponentRef } contract={contract} suggestions={suggestions} />
              ) : contract.contract_type === "소비대차" ? (
                <LoanContract ref={contractComponentRef } contract={contract} suggestions={suggestions} />
              ) : contract.contract_type === "매매" ? (
                <SaleContract ref={contractComponentRef } contract={contract} suggestions={suggestions} />
              ) : contract.contract_type === "사용대차" ? (
                <UsageLoanContract ref={contractComponentRef } contract={contract} suggestions={suggestions} />
              ) : (
                <p>지원되지 않는 계약서 유형입니다: {contract.contract_type}</p>
            )}
        </div>
        

        <div className="download-button-wrap">
          <button className="download-btn" onClick={handleSave}>💾 저장</button>
          <button className="download-btn" onClick={handleDownload}>⬇️ 다운로드</button>
          <button className="download-btn" onClick={handleRestore}>↩️ 되돌리기</button>
          <button className="download-btn danger" onClick={handleDelete}>🗑️ 삭제</button>
        </div>
      </main>
    </div>
  );
}

export default Contract_download;