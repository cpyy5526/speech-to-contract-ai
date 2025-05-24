import React, { useState, useRef } from "react";
import "../styles/Converting.css";
import { useNavigate } from "react-router-dom";
import { generateContract, getContractStatus, cancelContractGeneration } from "../services/contractApiMock";

function Converting() {
  const [status, setStatus] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const intervalRef = useRef(null); // ✅ polling 중단용 ref

  const startPolling = () => {
    intervalRef.current = setInterval(async () => {
      try {
        const result = await getContractStatus();
        setStatus(result.status);

        if (result.status === "done" && result.contract_id) {
          clearInterval(intervalRef.current);
          setLoading(false);
          navigate(`/download?contract_id=${result.contract_id}`);
        }

        if (result.status === "failed") {
          clearInterval(intervalRef.current);
          retryGenerate(); // ✅ 안전한 반복 호출
        }

        if (result.status === "cancelled") {
          clearInterval(intervalRef.current);
          setLoading(false);
          console.warn("⛔ 생성이 취소됨");
        }
      } catch (err) {
        clearInterval(intervalRef.current);
        setLoading(false);
        console.error("❌ 상태 확인 중 오류:", err.response?.data?.detail || err.message);
      }
    }, 3000);
  };

  const retryGenerate = async () => {
    console.warn("🔁 계약서 생성을 다시 시도합니다...");
    try {
      await generateContract();
      setStatus("generating");
      startPolling();
    } catch (err) {
      console.error("❌ 재시도 실패:", err.response?.data?.detail || err.message);
      setStatus("error");
      setLoading(false);
    }
  };



  const handleClick = async () => {
    setStatus("");
    setLoading(true);

    try {
      await generateContract();
      setStatus("generating");
      startPolling(); // 🔁 polling 시작
    } catch (err) {
      console.error("❌ 계약서 생성 요청 실패:", err.response?.data?.detail || err.message);
      setStatus("error");
      setLoading(false);
    }
  };


  const handleCancel = async () => {
    try {
      await cancelContractGeneration();
      console.log("📬 생성 중단 요청을 보냈습니다. 상태 확인 중...");
      // ✅ polling 유지: 다음 getContractStatus() 응답이 "cancelled"일 때 종료
    } catch (err) {
      console.error("❌ 취소 실패:", err.response?.data?.detail || err.message);
    }
  };


  return (
    <div className="converting-container">
      <p>음성을 글자로 변환 중입니다...</p>
      <button
        onClick={(status === "generating" || status === "failed") ? handleCancel : handleClick}
        disabled={loading && !(status === "generating" || status === "failed")}
      >
        {(status === "generating" || status === "failed") ? "생성 취소" : "계약서 생성"}
      </button>
      {status && <p>상태: {status}</p>}
    </div>
    
  );
}

export default Converting;
