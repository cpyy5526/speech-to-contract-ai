import React, { useEffect, useRef, useState } from "react";
import "../styles/Contract_download.css";
import contractImage from "../images/contract_icon.png";
import jsPDF from "jspdf";
import html2canvas from "html2canvas";
import { useLocation } from "react-router-dom";
import { getContractContent } from "../services/contractApiMock"; // ✅ 실제 contract 조회 API

function Contract_download() {
  const [contract, setContract] = useState(null);
  const contractRef = useRef();
  const location = useLocation();
  const params = new URLSearchParams(location.search);
  const contractId = params.get("contract_id");

  // useEffect(() => {
  //   const fetchContract = async () => {
  //     try {
  //       const result = await getContractContent(contractId);
  //       setContract(result);
  //     } catch (err) {
  //       console.error("계약서 불러오기 실패:", err.response?.data?.detail || err.message);
  //     }
  //   };

  //   if (contractId) fetchContract();
  // }, [contractId]);

  // const handleDownload = async () => {
  //   const element = contractRef.current;
  //   const canvas = await html2canvas(element, { scale: 2 });
  //   const imgData = canvas.toDataURL("image/png");

  //   const pdf = new jsPDF("p", "mm", "a4");
  //   const width = pdf.internal.pageSize.getWidth();
  //   const height = (canvas.height * width) / canvas.width;

  //   pdf.addImage(imgData, "PNG", 0, 0, width, height);
  //   pdf.save("contract.pdf");
  // };

  return (
    <div className="download-container">
      <aside className="sidebar">
        <h3 className="sidebar-title">계약서 작성 목록</h3>
        <ul className="contract-list">
          <li><span>2025-04-01</span> 문화계약서</li>
          <li><span>2025-03-27</span> 금융차용증서</li>
          <li><span>2025-03-25</span> 해외계약서</li>
          <li className="active"><span>2025-03-11</span> 부동산 임대차계약서</li>
        </ul>
      </aside>

      <main className="preview-area">
        <div className="contract-rendered" ref={contractRef}>
          {/* {contract ? (
            <>
              <h2>{contract.title}</h2>
              <p>{contract.body}</p>
            </>
          ) : (
            <p>계약서를 불러오는 중입니다...</p>
          )} */}
        </div>

        <div className="download-button-wrap">
          <button className="download-btn">
            계약서 다운로드
          </button>
          {/* <button className="download-btn" onClick={handleDownload}>
            계약서 다운로드
          </button> */}
        </div>
      </main>
    </div>
  );
}

export default Contract_download;
