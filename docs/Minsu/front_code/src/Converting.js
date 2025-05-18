import React from "react";
import "./Converting.css";
import exchangeIcon from "./images/exchange_icon.png";
import { useNavigate } from "react-router-dom";

function Converting() {
  const navigate = useNavigate();
  return (
    <div className="converting-container">
      
      <div className="center-content">
        <img src={exchangeIcon} className="exchange_icon"></img>
        <p>음성을 글자로 변환 중입니다...</p>
      </div>
      <button onClick={()=>navigate('/download')}>결과보기</button>
              
    </div>
  );
}

export default Converting;
