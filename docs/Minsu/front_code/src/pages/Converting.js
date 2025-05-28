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

  useEffect(() => {
    if (!uploadUrl || !audioBlob) {
      setStatus("error");
      return;
    }

    uploadFile(uploadUrl); // 최초 시작

    return () => {
      clearInterval(intervalRef.current);
      intervalRef.current = null;
    };
  }, [uploadUrl, audioBlob]);

  const uploadFile = async (urlToUse) => {
    try {
      await uploadAudioFile(urlToUse, audioBlob);
      console.log("📤 파일 업로드 요청 전송 완료");
      startPolling();
    } catch (err) {
      const detail = err.response?.data?.detail || err.message || err;
      console.error("❌ 업로드 요청 실패:", detail);

      try {
        console.log("🔁 업로드 예약 다시 시도 중...");
        const newUrl = await initiateTranscription(filename);
        console.log("📦 새 업로드 URL:", newUrl);

        await uploadAudioFile(newUrl, audioBlob);
        console.log("📤 재업로드 요청 전송 완료");
        startPolling();
      } catch (retryErr) {
        const retryDetail = retryErr.response?.data?.detail || retryErr.message || retryErr;
        console.error("❌ 업로드 재시도 실패:", retryDetail);
        setStatus("upload_failed");

        navigate("/recording");
      }
    }
  };



  const startPolling = () => {
    if (intervalRef.current) return; // 중복 방지

    intervalRef.current = setInterval(async () => {
      try {
        const { status: serverStatus } = await getTranscriptionStatus();
        console.log("📡 상태 확인:", serverStatus);

        // ✅ 자동 업로드 재시도 처리
        if (serverStatus === "upload_failed") {
          clearInterval(intervalRef.current);
          intervalRef.current = null;

          try {
            console.log("🔁 상태 polling 중: upload_failed → 재시도");
            const newUrl = await initiateTranscription(filename);
            await uploadAudioFile(newUrl, audioBlob);
            console.log("📦 재업로드 요청 전송 완료");
            setStatus("uploaded");
            startPolling(); // 다시 polling 시작
          } catch (retryErr) {
            const detail = retryErr.response?.data?.detail || retryErr.message || retryErr;
            console.error("❌ 자동 재시도 실패:", detail);
            setStatus("upload_failed"); // 재시도까지 실패
          }

          return; // ⚠️ 아래 코드 실행 안 되도록 조기 리턴
        }

        // ✅ 정상 종료 조건
        if (["done", "transcription_failed", "cancelled"].includes(serverStatus)) {
          clearInterval(intervalRef.current);
          intervalRef.current = null;
          setStatus(serverStatus);

          if (serverStatus === "done") {
            alert("✅ 변환이 완료되었습니다.");
            navigate("/generating");
          }

          if (serverStatus === "cancelled") {
            alert("⛔ 변환이 취소되었습니다.");
            navigate("/home");
          }

          return;
        }

        // ✅ 진행 중 상태
        setStatus(serverStatus); // uploading, uploaded, transcribing 등
      } catch (err) {
        console.error("❌ 상태 확인 실패:", err);
        clearInterval(intervalRef.current);
        intervalRef.current = null;
        setStatus("error");
      }
    }, 3000);
  };


  const handleRetry = async () => {
    try {
      await retryTranscription();
      console.log("🔁 재시도 요청 성공");
      setStatus("uploaded");
      startPolling(); // 다시 polling 시작
    } catch (err) {
      console.error("❌ 재시도 실패:", err);
      alert("재시도에 실패했습니다.");
    }
  };

  const handleCancel = async () => {
    try {
      await cancelTranscription();
      console.log("📭 중단 요청 전송됨 (상태는 서버에서 변경됨)");
      startPolling();
    } catch (err) {
      console.error("❌ 중단 요청 실패:", err);
      alert("중단 요청에 실패했습니다.");
    }
  };


  return (
  <div className="converting-container">
    <div className="center-content">
      {/* 회전 로딩 아이콘 */}
      {["uploading", "uploaded", "transcribing"].includes(status) && (
        <div className="spinner" />
      )}

      {/* 상태별 텍스트 메시지 */}
      {status === "uploading" && <p>📤 음성 파일 업로드 중입니다...</p>}
      {status === "uploaded" && <p>📦 업로드 완료! 텍스트로 변환 대기 중...</p>}
      {status === "transcribing" && <p>🧠 텍스트로 변환 중입니다...</p>}
      {status === "upload_failed" && <p>❌ 파일 업로드에 실패했습니다. 다시 시도합니다.</p>}
      {status === "transcription_failed" && (
        <>
          <p>❌ 텍스트 변환에 실패했습니다.</p>
          <button onClick={handleRetry}>🔁 다시 시도</button>
        </>
      )}
      {status === "cancelled" && <p>⛔ 변환이 취소되었습니다.</p>}
      {status === "error" && <p>⚠️ 알 수 없는 오류가 발생했습니다.</p>}

      {/* ✅ 중단 버튼 */}
      {["uploading", "uploaded", "transcribing", "transcription_failed"].includes(status) && (
        <button onClick={handleCancel}>🛑 중단</button>
      )}
    </div>
  </div>
  );

}

export default Converting;
