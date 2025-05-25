import React, { useEffect, useRef, useState } from "react";
import "../styles/Recording.css";
import { useNavigate } from "react-router-dom";
import { initiateTranscription } from "../services/convertApiMock"; // 배포 시 convertApi로


function Recording() {
  const [isRecording, setIsRecording] = useState(false);
  const [isStopped, setIsStopped] = useState(false);
  const [seconds, setSeconds] = useState(0);
  const [audioBlob, setAudioBlob] = useState(null);
  const mediaRecorderRef = useRef(null);
  const audioChunks = useRef([]);
  const navigate = useNavigate();

  useEffect(() => {
    let timer;
    if (isRecording) {
      timer = setInterval(() => setSeconds((s) => s + 1), 1000);
    }
    return () => clearInterval(timer);
  }, [isRecording]);

  useEffect(() => {
    startRecording();
  }, []);

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const recorder = new MediaRecorder(stream);
      mediaRecorderRef.current = recorder;

      recorder.ondataavailable = (e) => audioChunks.current.push(e.data);
      recorder.onstop = () => {
        const blob = new Blob(audioChunks.current, { type: "audio/webm" });
        setAudioBlob(blob);
        audioChunks.current = [];
      };

      recorder.start();
      setIsRecording(true);
      setIsStopped(false);
      setSeconds(0);
    } catch (err) {
      alert("마이크 권한을 허용해주세요");
    }
  };

  const stopRecording = () => {
    mediaRecorderRef.current?.stop();
    setIsRecording(false);
    setIsStopped(true);
  };

  const handleFinish = async () => {
    if (!audioBlob) return;

    try {
      const filename = `recording_${Date.now()}.webm`;
      const result = await initiateTranscription(filename);
      const uploadUrl = result.upload_url;

      console.log("✅ 업로드 예약 완료:", uploadUrl);

      // Converting 페이지로 uploadUrl 전달
      navigate("/converting", { state: { uploadUrl, audioBlob } }); // audioBlob도 함께 넘길 수 있음
    } catch (err) {
      console.error("❌ 업로드 예약 실패:", err);
      alert("업로드 예약 중 오류가 발생했습니다.");
    }
  };



  return (
    <div className="recording-container">
      

      <div className="recording-content">
        <div className="listening-text">듣는 중...</div>
        <div className="mic-section">
          <div className="mic-icon">🎤</div>
          <div className="timer">
            {String(Math.floor(seconds / 60)).padStart(2, "0")}:
            {String(seconds % 60).padStart(2, "0")}
          </div>
        </div>
      </div>

      {isStopped && audioBlob && (
          <div className="preview-section">
            <p>녹음 미리 듣기:</p>
            <audio controls src={URL.createObjectURL(audioBlob)} />
          </div>
      )}
      
      <div className="recording-buttons">
        {isRecording ? (
          <button className="stop-btn" onClick={stopRecording}>🟥 녹음 중단</button>
        ) : (
          <>
            {isStopped && (
              <>
                <button className="stop-btn" onClick={startRecording}>🔁 재시작</button>
                <button className="finish-btn" onClick={handleFinish}>✅ 텍스트로 변환하기</button>
              </>
            )}
          </>
        )}
      </div>
    </div>
  );
}

export default Recording;
