// services/convertApi.js
import api from "./apiClient";

/**
 * 음성 업로드 예약 요청
 * @param {string} filename - 예: "recording.wav"
 * @returns {Promise<string>} - 업로드용 pre-signed URL
 */
export async function initiateTranscription(filename) {
  try {
    const response = await api.post("/transcription/initiate", { filename });

    if (response.status === 202) {
      return response.data.upload_url;
    }
  } catch (error) {
    const status = error.response?.status;
    const detail = error.response?.data?.detail || "응답 없음";

    if (status === 400) {
      if (detail === "Missing file name") {
        alert("❗ 파일명이 누락되었습니다.");
      } else {
        alert(`❗ 요청 오류: ${detail}`);
      }
    } else if (status === 415) {
      if (detail === "Unsupported audio format") {
        alert("❗ 지원되지 않는 오디오 파일 형식입니다.");
      } else {
        alert(`❗ 형식 오류: ${detail}`);
      }
    } else if (status === 500) {
      alert("⚠️ 서버 오류가 발생했습니다. 잠시 후 다시 시도해주세요.");
    } else {
      alert(`❌ 오류 발생: ${status}`);
    }

    throw error;
  }
}


/**
 * 업로드 서버에 음성 파일 전송 (pre-signed upload_url 사용)
 * @param {string} uploadUrl - initiateTranscription()에서 받은 URL
 * @param {Blob} audioBlob - 업로드할 음성 파일 Blob
 * @returns {Promise<void>}
 */
export async function uploadAudioFile(uploadUrl, audioBlob) {
  try {
    const response = await fetch(uploadUrl, {
      method: "PUT",
      headers: {
        "Content-Type": "application/octet-stream",
      },
      body: audioBlob,
    });

    const status = response.status;
    if (status === 204) return
    let detail = "응답 없음";

    try {
      const errorBody = await response.json();
      detail = errorBody?.detail || detail;
    } catch {
      // JSON 파싱 실패는 무시
    }

    if (status === 400) {
      if (detail === "Invalid or expired upload_url") {
        alert("❗ 파일명이 누락되었습니다.");
      } else {
        alert(`❗ 요청 오류: ${detail}`);
      }
    } else if (status === 413) {
      if (detail === "Audio file is too large") {
        alert("❗ 파일 용량이 너무 큽니다.");
      }
    } else if (status === 415) {
      if (detail === "Unsupported audio format") {
        alert("❗ 허용되지 않는 파일 형식입니다.");
      } else {
        alert(`❗ 형식 오류: ${detail}`);
      }
    } else if (status === 500) {
      alert("⚠️ 서버 오류가 발생했습니다. 잠시 후 다시 시도해주세요.");
    } else {
      alert(`❌ 오류 발생: ${status}`);
    }
    throw new Error(`Upload failed: status ${status}`);
  } catch (error) {
    alert("⛔ 네트워크 오류 또는 예기치 않은 문제 발생");
    throw error;
  }
}

/**
 * 음성 텍스트 변환 상태 조회
 * @returns {Promise<{ status: string }>}
 */
export async function getTranscriptionStatus() {
  try {
    const response = await api.get("/transcription/status");
    return response.data; // 예: { status: "transcribing" }
  } catch (error) {
    const status = error.response?.status;
    const detail = error.response?.data?.detail || "응답 없음";

    if (status === 404) {
      if (detail === "No audio data for this user") {
        alert("❗ 업로드 요청이 없거나 만료되었습니다.");
        window.location.href = "/";
      } else {
        alert(`❗ 요청 오류: ${detail}`);
      }
    } else if (status === 500) {
      alert("⚠️ 서버 오류가 발생했습니다. 잠시 후 다시 시도해주세요.");
    } else {
      alert(`❌ 오류 발생: ${status}`);
    }

    throw error;
  }
}


/**
 * 텍스트 변환 재시도 요청 (status가 transcription_failed일 때만 가능)
 * @returns {Promise<void>}
 */
export async function retryTranscription() {
  try {
    const response = await api.get("/transcription/retry");

    if (response.status === 202) {
    }
  } catch (error) {
    const status = error.response?.status;
    const detail = error.response?.data?.detail || "응답 없음";

    if (status === 404) {
      if (detail === "No audio data for this user") {
        alert("❗ 업로드 요청이 없거나 만료되었습니다.");
        window.location.href = "/";
      } else {
        alert(`❗ 요청 오류: ${detail}`);
      }
    }else if (status === 409) {
      if (detail === "Cannot retry at this stage") {
        alert("❗ 재시도 가능한 상태가 아닙니다.");
      } else {
        alert(`❗ 요청 오류: ${detail}`);
      }
    } else if (status === 500) {
      alert("⚠️ 서버 오류가 발생했습니다. 잠시 후 다시 시도해주세요.");
    } else {
      alert(`❌ 오류 발생: ${status}`);
    }

    throw error;
  }
}



/**
 * 업로드 또는 텍스트 변환 중단 요청
 * @returns {Promise<void>}
 */
export async function cancelTranscription() {
  try {
    const response = await api.post("/transcription/cancel");

    if (response.status === 204) {
      return;
    }

    // 204 외의 응답이 올 경우 대비 (안전망)
    throw new Error(`Unexpected response status: ${response.status}`);
  } catch (error) {
    const status = error.response?.status;
    const detail = error.response?.data?.detail || "응답 없음";

    if (status === 404) {
      if (detail === "No audio data for this user") {
        alert("❗ 업로드 요청이 없거나 만료되었습니다.");
        window.location.href = "/";
        
      } else {
        alert(`❗ 요청 오류: ${detail}`);
      }
    }else if (status === 409) {
      if (detail === "Cannot retry at this stage") {
        alert("❗ 취소 가능한 상태가 아닙니다.");
      } else {
        alert(`❗ 요청 오류: ${detail}`);
      }
    } else if (status === 500) {
      alert("⚠️ 서버 오류가 발생했습니다. 잠시 후 다시 시도해주세요.");
    } else {
      alert(`❌ 오류 발생: ${status}`);
    }

    throw error;
  }
}
