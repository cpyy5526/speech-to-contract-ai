import React, { useEffect, useRef, useState } from "react";
import "../styles/Recording.css";
import { useNavigate } from "react-router-dom";
import { initiateTranscription } from "../services/convertApi"; // 배포 시 convertApi로


function Recording() {
  const [isRecording, setIsRecording] = useState(false);
  const [isStopped, setIsStopped] = useState(false);
  const [seconds, setSeconds] = useState(0);
  const [audioBlob, setAudioBlob] = useState(null);
  const [mediaStream, setMediaStream] = useState(null);
  const shouldSaveToLocalRef = useRef(true);

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

        if (shouldSaveToLocalRef.current) {
          const confirmSave = window.confirm("녹음 파일을 저장하시겠습니까?");
          if (confirmSave) {
            saveToLocal(blob, `recording_${Date.now()}.webm`);
          }
        }
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
      mediaStream.getTracks().forEach((track) => {
        track.stop();
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

  const handleFinish = async () => {
    if (!audioBlob) return;
    shouldSaveToLocalRef.current = false;

    const finalize = async () => {
      try {
        const filename = `recording_${Date.now()}.webm`;

        if (!filename || typeof filename !== "string" || filename.trim() === "") {
          alert("파일명이 유효하지 않습니다.");
          return;
        }

        const result = await initiateTranscription(filename);
        const uploadUrl = result.upload_url;

        // Converting 페이지로 uploadUrl과 audioBlob 전달
        navigate("/converting", { state: { uploadUrl, audioBlob, filename } });
      } catch (err) {
        // 에러 처리는 authApi에서 처리됨
      }
    };

    if (mediaRecorderRef.current && mediaRecorderRef.current.state !== "inactive") {
      mediaRecorderRef.current.onstop = finalize;
      mediaRecorderRef.current.stop(); // MediaRecorder 종료 요청
      stopMediaStream(); // 스트림 정리
    } else {
      stopMediaStream(); // 이미 정지된 경우 바로 실행
      await finalize();
    }

  };


  const saveToLocal = (blob, filename = "recording.webm") => {
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = filename;
    a.click();
    URL.revokeObjectURL(url); // 메모리 해제
  };



  return (
    <div className="recording-container">
      

      {isRecording ? (
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
      ) : (
        <div className="recording-content">
          <div className="listening-text">녹음이 중단되었습니다</div>
          <div className="timer"> 
              {String(Math.floor(seconds / 60)).padStart(2, "0")}:
              {String(seconds % 60).padStart(2, "0")}
            </div>
        </div>
      )}


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
