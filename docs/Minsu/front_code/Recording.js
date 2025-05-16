import React, { useEffect, useRef, useState } from "react";
import "./Recording.css";
import { useNavigate } from "react-router-dom";

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

  const handleFinish = () => {
    console.log("녹음 완료된 파일:", audioBlob);
    navigate("/converting");
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
                <button className="finish-btn" onClick={handleFinish}>✅ 마무리</button>
              </>
            )}
          </>
        )}
      </div>
    </div>
  );
}

export default Recording;
