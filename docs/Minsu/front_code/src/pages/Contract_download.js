import React, { useEffect, useRef, useState } from "react";
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
} from "../services/contractApiMock";

import GiftContract from "../Contract_types/GiftContract";
import ConstructionContract from "../Contract_types/ConstructionContract";
import EmploymentContract from "../Contract_types/EmploymentContract";
import ExchangeContract from "../Contract_types/ExchangeContract";
import LeaseContract from "../Contract_types/LeaseContract";
import LoanContract from "../Contract_types/LoanContract";
import SaleContract from "../Contract_types/SaleContract";
import UsageLoanContract from "../Contract_types/UsageLoanContract";



function Contract_download() {
  const [contract, setContract] = useState(null);
  const [contractList, setContractList] = useState([]);
  const [suggestions, setSuggestions] = useState([]);

  const contractRef = useRef();
  const giftContractRef = useRef();
  const location = useLocation();

  const params = new URLSearchParams(location.search);
  const contractId = params.get("contract_id");

  const navigate = useNavigate();

  

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

  useEffect(() => {
      if (contractId) fetchContract();
  }, [contractId]);

  const fetchContract = async () => {
    try {
      const result = await getContractContent(contractId);
      setContract(result);

      const suggestionResult = await getSuggestions(contractId);
      setSuggestions(suggestionResult);
    } catch (err) {
      console.error("계약서 불러오기 실패:", err.response?.data?.detail || err.message);
    }
  };

  const handleSave = async () => {
    try {
    const edited = giftContractRef.current.extract();
      await updateContractContent(contractId, edited);
    } catch (err) {
      console.error("❌ 저장 실패:", err);
    }
  };


  const handleDownload = async () => {
  const el = contractRef.current;
  if (!el) return alert("계약서가 렌더링되지 않았습니다.");

  // 1) 원본에 영향을 주지 않는 클론 생성
  const clone = el.cloneNode(true);
  clone.classList.add("fullscreen");                // ← 여기가 핵심!
  Object.assign(clone.style, {
    position:  "absolute",
    top:       "-9999px",
    left:      "-9999px",
    width:     `${el.scrollWidth}px`,
    background:"white",
  });
  document.body.appendChild(clone);

  // 2) 충분히 렌더링 안정화 대기
  await new Promise(r => setTimeout(r, 100));

  // 3) html2canvas 로 full-height 캡처
  const canvas = await html2canvas(clone, {
    scale:       2,
    useCORS:     true,
    allowTaint:  true,
    width:       clone.scrollWidth,
    height:      clone.scrollHeight,
    scrollX:     0,
    scrollY:     0
  });

  // 4) 클론 제거
  document.body.removeChild(clone);

  // 5) jsPDF 로 A4 multiple-page 처리
  const pdf  = new jsPDF("p", "mm", "a4");
  const pdfW = pdf.internal.pageSize.getWidth();
  const pdfH = pdf.internal.pageSize.getHeight();
  // 픽셀→mm 비율
  const pxPerMm = canvas.width / pdfW;
  let imgHmm = canvas.height / pxPerMm;  // 전체 이미지 높이를 mm 단위로
  let yPos   = 0;

  const imgData = canvas.toDataURL("image/png");
  // 페이지 단위로 잘라 넣기
  while (yPos < imgHmm) {
    const hThisPage = Math.min(imgHmm - yPos, pdfH);
    pdf.addImage(
      imgData,
      "PNG",
      0,          // x(mm)
      -yPos,      // y(mm) 음수 오프셋으로 위에서부터 잘라서 그리기
      pdfW,
      imgHmm
    );
    yPos += pdfH;
    if (yPos < imgHmm) pdf.addPage();
  }

  pdf.save("contract.pdf");
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
      <aside className="sidebar">
        <button
          onClick={() => navigate("/home")}
          className="go-home-btn"
        >
          ⬅ 메인페이지
        </button>
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


      <main className="preview-area">
        <div className="contract-rendered" ref={contractRef}>
          {!contract ? (
            <p>계약서를 불러오는 중입니다...</p>
              ) : contract.contract_type === "증여 계약" ? (
                <GiftContract ref={giftContractRef} contract={contract} suggestions={suggestions} />
              ) : contract.contract_type === "공사 계약" ? (
                <ConstructionContract ref={giftContractRef} contract={contract} suggestions={suggestions} />
              ) : contract.contract_type === "고용 계약" ? (
                <EmploymentContract ref={giftContractRef} contract={contract} suggestions={suggestions} />
              ) : contract.contract_type === "교환 계약" ? (
                <ExchangeContract ref={giftContractRef} contract={contract} suggestions={suggestions} />
              ) : contract.contract_type === "임대차 계약" ? (
                <LeaseContract ref={giftContractRef} contract={contract} suggestions={suggestions} />
              ) : contract.contract_type === "금전 대여 계약" ? (
                <LoanContract ref={giftContractRef} contract={contract} suggestions={suggestions} />
              ) : contract.contract_type === "매매 계약" ? (
                <SaleContract ref={giftContractRef} contract={contract} suggestions={suggestions} />
              ) : contract.contract_type === "사용대차 계약" ? (
                <UsageLoanContract ref={giftContractRef} contract={contract} suggestions={suggestions} />
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