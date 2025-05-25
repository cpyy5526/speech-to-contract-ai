import React, { useEffect, useRef, useState } from "react";
import "./Recording.css";
import { useNavigate } from "react-router-dom";

function Recording() {
  const [isRecording, setIsRecording] = useState(false);
  const [isStopped, setIsStopped] = useState(false);
  const [seconds, setSeconds] = useState(0);
  const [audioBlob, setAudioBlob] = useState(null);
  const [mediaStream, setMediaStream] = useState(null);
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

  
  return () => {
    console.log("🧹 언마운트 시 마이크 정리");

    if (mediaRecorderRef.current?.state === "recording") {
      mediaRecorderRef.current.stop();
    }

    if (window.streamsToClose) {
      window.streamsToClose.forEach((stream) => {
        stream.getTracks().forEach((track) => {
          console.log(" [cleanup] 전역 스트림 종료", track);
          track.stop();
        });
      });
      window.streamsToClose = [];
    }
  };
}, []);

  const startRecording = async () => {
  if (mediaStream) {
    console.log(" 이미 mediaStream 존재함. 중복 방지");
    return;
  }

  try {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });

    // 
    window.streamsToClose = window.streamsToClose || [];
    window.streamsToClose.push(stream);

    const recorder = new MediaRecorder(stream);
    mediaRecorderRef.current = recorder;
    setMediaStream(stream);

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


  const stopMediaStream = () => {
  if (mediaStream) {
    console.log("🛑 마이크 트랙 종료 시도:", mediaStream.getTracks());
    mediaStream.getTracks().forEach((track) => {
      console.log(`🧨 종료 전 상태: kind=${track.kind}, enabled=${track.enabled}, readyState=${track.readyState}`);
      track.stop();
      console.log(`✅ 종료 후 상태: kind=${track.kind}, enabled=${track.enabled}, readyState=${track.readyState}`);
    });
    setMediaStream(null);
  } else {
    console.log("⚠️ 종료할 mediaStream 없음");
  }
};

  const stopRecording = () => {
    mediaRecorderRef.current?.stop();
    stopMediaStream(); // 마이크 종료
    setIsRecording(false);
    setIsStopped(true);
  };

  const handleFinish = () => {
  if (mediaRecorderRef.current && mediaRecorderRef.current.state !== "inactive") {
    mediaRecorderRef.current.onstop = () => {
      stopMediaStream(); // 스트림 정리
      navigate("/converting"); // 녹음 멈춘 뒤 이동
    };
    mediaRecorderRef.current.stop(); // MediaRecorder 종료 요청
  } else {
    stopMediaStream(); // 만약 이미 stop된 경우 바로 정리
    navigate("/converting");
  }
};
  const forceStopAllMedia = async () => {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    stream.getTracks().forEach((track) => {
      console.log("🔧 강제 종료 트랙:", track);
      track.stop();
    });
  } catch (err) {
    console.log("❌ 강제 종료 실패", err);
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
