import React, { useEffect, useRef, useState } from "react";
import "../styles/Contract_download.css";
import contractImage from "../images/contract_icon.png";
import jsPDF from "jspdf";
import html2canvas from "html2canvas";
import { useLocation } from "react-router-dom";
import { getContractContent } from "../services/contractApiMock"; // ✅ 실제 contract 조회 API
import { getContractList } from "../services/contractApiMock";
import { updateContractContent } from "../services/contractApiMock";
import { getSuggestions } from "../services/contractApiMock";
import { restoreContract } from "../services/contractApiMock"; // 배포 시 contractApi로 변경
import { deleteContract } from "../services/contractApiMock"; // 실제 배포 시 contractApi로 변경

import GiftContract from "../Contract_types/GiftContract";
import { useNavigate } from "react-router-dom";



function Contract_download() {
  const [contract, setContract] = useState(null);
  const [contractList, setContractList] = useState([]);
  const [suggestions, setSuggestions] = useState([]);
  const contractRef = useRef();
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
      const edited = contractRef.current.extract(); // ✅ 정확하고 안전
      await updateContractContent(contractId, edited);
    } catch (err) {
      console.error("❌ 저장 실패:", err);
    }
  };


  const handleDownload = async () => {
    const element = contractRef.current;
    const canvas = await html2canvas(element, { scale: 2 });
    const imgData = canvas.toDataURL("image/png");

    const pdf = new jsPDF("p", "mm", "a4");
    const width = pdf.internal.pageSize.getWidth();
    const height = (canvas.height * width) / canvas.width;

    pdf.addImage(imgData, "PNG", 0, 0, width, height);
    pdf.save("contract.pdf");
  };

  const handleRestore = async () => {
    if (!window.confirm("⚠️ 초기 생성 상태로 되돌리시겠습니까? 변경된 내용은 모두 사라집니다.")) return;

    try {
      await restoreContract(contractId);
      alert("복구 완료");
      fetchContract(); // ← 이거 다시 호출
    } catch (err) {
      console.error("❌ 복구 실패:", err.response?.data?.detail || err.message);
    }
  };

  const handleDelete = async () => {
    if (!window.confirm("🗑️ 정말 이 계약서를 삭제하시겠습니까? 삭제 후 되돌릴 수 없습니다.")) return;

    try {
      await deleteContract(contractId);
      alert("✅ 계약서가 삭제되었습니다.");

      // 리스트에서 삭제된 항목 제거
      setContractList((prevList) => prevList.filter(item => item.id !== contractId));

      // 현재 열려 있던 계약서도 닫기
      setContract(null);
      navigate("/download"); // URL 초기화 (선택 안 된 상태로)
    } catch (err) {
      console.error("❌ 삭제 실패:", err.response?.data?.detail || err.message);
    }
  };



  return (
    <div className="download-container">
      <aside className="sidebar">
        <h3 className="sidebar-title">계약서 작성 목록</h3>
        <ul className="contract-list">
          {contractList.map((item) => (
            <li
              key={item.id}
              className={item.id === contractId ? "active" : ""}
              onClick={() => navigate(`/download?contract_id=${item.id}`)} // ✅ 클릭 시 이동
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
            <GiftContract ref={contractRef} contract={contract} suggestions={suggestions}/>
          ) : (
            <p>지원되지 않는 계약서 유형입니다: {contract.contract_type}</p>
          )}
        </div>
        
        


        <div className="download-button-wrap">
          <button onClick={handleSave}>계약서 저장</button>
          <button className="download-btn" onClick={handleDownload}>계약서 다운로드</button>
          <button onClick={handleRestore}>되돌리기</button>
          <button onClick={handleDelete} style={{ color: "red" }}>삭제</button> {/* ✅ 삭제 버튼 */}
        </div>


      </main>
    </div>
  );
}

export default Contract_download;
