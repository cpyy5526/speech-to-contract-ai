import React, { useEffect, useState, useRef } from "react";
import "../styles/Converting.css";
import { useLocation, useNavigate } from "react-router-dom";
import {
  initiateTranscription,
  uploadAudioFile,
  getTranscriptionStatus,
  retryTranscription,
  cancelTranscription,
} from "../services/convertApiMock";

function Converting() {
  const location = useLocation();
  const navigate = useNavigate();

  const uploadUrl = location.state?.uploadUrl;
  const audioBlob = location.state?.audioBlob;
  const filename = location.state?.filename || `recording_${Date.now()}.webm`;

  const [status, setStatus] = useState("uploading");
  const intervalRef = useRef(null);

  const clearPolling = () => {
    if (intervalRef.current){
      clearInterval(intervalRef.current);
      intervalRef.current = null;
    }
  };

  const uploadFile = async (urlToUse) => {
    try {
      await uploadAudioFile(urlToUse, audioBlob);
      startPolling();
    } catch (err) {
      console.error("❌ 업로드 실패:", err);
      navigate("/home"); // 실패 시 즉시 홈 이동
    }
  };


  const startPolling = () => {
    if (intervalRef.current) return; // 중복 방지

    intervalRef.current = setInterval(async () => {
      try {
        const { status: serverStatus } = await getTranscriptionStatus();

        if (serverStatus === "upload_failed") {
          clearPolling();
          setStatus("upload_failed");
          return;
        }

        if (["done", "transcription_failed", "cancelled"].includes(serverStatus)) {
          clearPolling();
          setStatus(serverStatus);

          if (serverStatus === "done") {
            navigate("/generating");
          } else if(serverStatus === "cancelled"){
            alert("⛔ 변환이 취소되었습니다.");
            navigate("/home");
          }

          return;
        }

        setStatus(serverStatus); 
      } catch (err) {
        clearPolling();
        setStatus("error");
      }
    }, 3000);
  };


  const handleRetry = async () => {
    try {
      await retryTranscription();
      setStatus("uploaded");
      startPolling();
    } catch (err) {
       // 에러 처리는 convertApi에서 처리됨
       setStatus("error");
    }
  };

  const handleCancel = async () => {
    try {
      await cancelTranscription();
      if (!intervalRef.current) {
        startPolling();
      }
    } catch (err) {
      // 에러 처리는 convertApi에서 처리됨
      setStatus("error");
    }
  };

  const handleRetryUpload = async () => {
  try {
    const newUrl = await initiateTranscription(filename);
    await uploadAudioFile(newUrl, audioBlob);
    setStatus("uploaded");
    startPolling();
  } catch (err) {
    console.error("❌ 업로드 재시도 실패:", err);
    setStatus("upload_failed"); // 여전히 실패하면 유지
  }
};




  useEffect(() => {
    if (!uploadUrl || !audioBlob) {
      setStatus("error");
      return;
    }

    uploadFile(uploadUrl);

    return () => {
      clearPolling();
    };
  }, [uploadUrl, audioBlob]);


  return (
  <div className="converting-container">
    <div className="center-content">
      {["uploading", "uploaded", "transcribing"].includes(status) && (
        <div className="spinner" />
      )}

      {status === "uploading" && <p>📤 음성 파일 업로드 중입니다...</p>}
      {status === "uploaded" && <p>📦 업로드 완료! 텍스트로 변환 대기 중...</p>}
      {status === "transcribing" && <p>🧠 텍스트로 변환 중입니다...</p>}
      {status === "upload_failed" && (
        <>
          <p>❌ 파일 업로드에 실패했습니다.</p>
          <button onClick={handleRetryUpload}>🔁 다시 업로드 시도</button>
        </>
      )}
      {status === "transcription_failed" && (
        <>
          <p>❌ 텍스트 변환에 실패했습니다.</p>
          <button onClick={handleRetry}>🔁 다시 시도</button>
        </>
      )}
      {status === "cancelled" && <p>⛔ 변환이 취소되었습니다.</p>}
      {status === "error" && <p>⚠️ 알 수 없는 오류가 발생했습니다.</p>}

      {["uploading", "uploaded", "transcribing", "transcription_failed"].includes(status) && (
        <button onClick={handleCancel}>🛑 중단</button>
      )}
    </div>
  </div>
  );
}

export default Converting;
