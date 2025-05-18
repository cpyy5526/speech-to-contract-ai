import React, { useRef } from "react";
import "./Contract_download.css";
import contractImage from "./images/contract_icon.png"
import jsPDF from "jspdf";
import html2canvas from "html2canvas";




const dummyData = {
  contract_type: "부동산 임대차계약서",
  contract_date: "2025-03-11",
  contractor: {
    name: "홍길동",
    address: "서울시 강남구 테헤란로 123"
  },
  contractee: {
    name: "김영희",
    address: "서울시 서초구 반포대로 456"
  },
  details: "본 계약은 임대인과 임차인 간의 합의에 따라 작성되었으며..."
};

function Contract_download() {
  const contract = dummyData;

  const contractRef = useRef(); // 📌 계약서 영역 참조용

  const handleDownload = async () => {
    const element = contractRef.current;
    const canvas = await html2canvas(element, { scale: 2 });
    const imgData = canvas.toDataURL("image/png");

    const pdf = new jsPDF("p", "mm", "a4");
    const width = pdf.internal.pageSize.getWidth();
    const height = (canvas.height * width) / canvas.width;

    pdf.addImage(imgData, "PNG", 0, 0, width, height);
    pdf.save("contract.pdf");

  }

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
          <h2>{contract.contract_type}</h2>
          <p><strong>계약일:</strong> {contract.contract_date}</p>
          <p><strong>계약자:</strong> {contract.contractor.name} ({contract.contractor.address})</p>
          <p><strong>피계약자:</strong> {contract.contractee.name} ({contract.contractee.address})</p>
          <p><strong>계약 내용:</strong><br />{contract.details}</p>
        </div>

        <div className="download-button-wrap">
          <button className="download-btn" onClick={handleDownload}>계약서 다운로드</button>
        </div>
      </main>
    </div>
  );
}

export default Contract_download;
