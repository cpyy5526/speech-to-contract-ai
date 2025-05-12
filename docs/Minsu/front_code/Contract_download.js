import React from "react";
import "./Contract_download.css";
import contractImage from "./images/contract_icon.png"

function Contract_download() {
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
        <div className="contract-image-wrap">
          <img src={contractImage} alt="계약서 이미지" className="contract-image" />
        </div>

        <div className="download-button-wrap">
          <button className="download-btn">계약서 다운로드</button>
        </div>
      </main>
    </div>
  );
}

export default Contract_download;
