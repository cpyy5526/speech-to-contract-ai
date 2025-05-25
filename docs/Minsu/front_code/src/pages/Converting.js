import React, { useState } from "react";
import "../styles/Converting.css";
import { useNavigate } from "react-router-dom";
import { initiateTranscription } from "../services/convertApiMock"; 


function Converting() {
  const [uploadUrl, setUploadUrl] = useState(null);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleUpload = async () => {
    setLoading(true);
    try {
      const filename = "recording.wav"; // 실제 파일에서 추출하면 더 좋음
      const result = await initiateTranscription(filename);
      console.log("✅ 업로드 URL:", result.upload_url);
      setUploadUrl(result.upload_url);

      // 실제 파일 업로드 단계는 여기서 추가 예정
      // 업로드 완료되면 다음 단계로 이동
      navigate("/generate"); // Contract_generate.js로 이동
    } catch (err) {
      console.error("❌ 업로드 예약 실패:", err.response?.data?.detail || err.message);
      alert("업로드 예약에 실패했습니다.");
    }
    setLoading(false);
  };

  return (
    <div className="converting-container">
      <p>음성 파일을 업로드할 준비가 되었습니다.</p>
      <button onClick={handleUpload} disabled={loading}>
        {loading ? "업로드 중..." : "업로드 시작"}
      </button>
      {uploadUrl && <p>업로드 URL: {uploadUrl}</p>}
    </div>
  );
}

export default Converting;
