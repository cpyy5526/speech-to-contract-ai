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
import GiftContract from "../Contract_types/GiftContract";



function Contract_download() {
  const [contract, setContract] = useState(null);
  const [contractList, setContractList] = useState([]);
  const [suggestions, setSuggestions] = useState([]);
  const contractRef = useRef();
  const location = useLocation();
  const params = new URLSearchParams(location.search);
  const contractId = params.get("contract_id");
  

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

    if (contractId) fetchContract();
  }, [contractId]);

 

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

  return (
    <div className="download-container">
      <aside className="sidebar">
        <h3 className="sidebar-title">계약서 작성 목록</h3>
        <ul className="contract-list">
          {contractList.map((item) => (
            <li key={item.id} className={item.id === contractId ? "active" : ""}>
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
          <button className="download-btn" onClick={handleDownload}>
            계약서 다운로드
          </button>
        </div>
      </main>
    </div>
  );
}

export default Contract_download;
