import React, { useState, useRef, useEffect } from "react";
import "../styles/Contract_generate.css";
import { useNavigate } from "react-router-dom";
import {
  generateContract,
  getContractStatus,
  cancelContractGeneration,
} from "../services/contractApiMock";

function ContractGenerate() {
  const [status, setStatus] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const intervalRef = useRef(null);

  const clearPolling = () => {
    if (intervalRef.current) {
      clearInterval(intervalRef.current);
      intervalRef.current = null;
    }
  };

  const startPolling = () => {
    if (intervalRef.current) return;

    intervalRef.current = setInterval(async () => {
      try {
        const result = await getContractStatus();
        setStatus(result.status);

        if (result.status === "done" && result.contract_id) {
          clearPolling();
          setLoading(false);
          navigate(`/download?contract_id=${result.contract_id}`);
        }

        if (result.status === "failed") {
          clearPolling();
          retryGenerate();
        }

        if (result.status === "cancelled") {
          clearPolling();
          setLoading(false);
          alert("⛔ 변환이 취소되었습니다.");
          navigate("/home");
        }
      } catch (err) {
        clearPolling();
        setLoading(false);
        setStatus("error");
      }
    }, 3000);
  };

  const retryGenerate = async () => {
    try {
      await generateContract();
      setStatus("generating");
      startPolling();
    } catch (err) {
      setStatus("error");
      setLoading(false);
    }
  };

  const handleClick = async () => {
    clearPolling();
    setStatus("");
    setLoading(true);

    try {
      await generateContract();
      setStatus("generating");
      startPolling();
    } catch (err) {
      setStatus("error");
      setLoading(false);
    }
  };

  const handleCancel = async () => {
    try {
      await cancelContractGeneration();
      clearPolling();
      setLoading(false);
      setStatus("cancelled");
    } catch (err) {
      // 에러 처리는 contractApi에서 처리됨
    }
  };

  useEffect(() => {
    handleClick();

    return () => {
      clearPolling();
    };
  }, []);

  return (
    <div className="contract-generate-container">
      <div className="contract-content">
        {/* Spinner */}
        {status === "generating" && <div className="contract-spinner" />}

        {/* 상태 메시지 */}
        {status === "generating" && <p>📄 계약서를 생성 중입니다...</p>}
        {status === "failed" && <p>❌ 생성 실패. 다시 시도합니다...</p>}
        {status === "cancelled" && <p>⛔ 생성이 취소되었습니다.</p>}
        {status === "error" && <p>⚠️ 오류 발생</p>}
        {!status && <p>📝 계약서 생성을 준비중입니다...</p>}

        {/* 버튼 */}
        {(status === "generating" || status === "failed") && (
          <button onClick={handleCancel}>🛑 생성 취소</button>
        )}
      </div>
    </div>
  );
}

export default ContractGenerate;