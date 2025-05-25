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
      console.log("✅ 업로드 예약 성공 (202 Accepted)");
      return response.data.upload_url;
    }
  } catch (error) {
    const { status, detail } = error.response?.data || {};

    switch (status) {
      case 400:
        alert("❗ 파일명이 누락되었습니다.");
        break;

      case 401:
        alert("🔒 인증이 필요합니다. 다시 로그인해주세요.");
        break;

      case 415:
        alert("❗ 지원되지 않는 오디오 파일 형식입니다.");
        break;

      case 500:
        alert("⚠️ 서버 오류가 발생했습니다. 잠시 후 다시 시도해주세요.");
        break;

      default:
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

    if (response.status === 204) {
      console.log("✅ 파일 업로드 성공 (204 No Content)");
    } else {
      console.warn("⚠️ 예상 외 응답:", response.status);
      throw new Error(`Upload failed: status ${response.status}`);
    }
  } catch (error) {
    console.error("❌ 파일 업로드 중 오류:", error);
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
    const { status, detail } = error.response?.data || {};

    switch (status) {
      case 401:
        alert("🔒 인증이 필요합니다. 다시 로그인해주세요.");
        break;
      case 404:
        alert("❗ 업로드된 음성 파일을 찾을 수 없습니다.");
        break;
      case 500:
        alert("⚠️ 서버 오류가 발생했습니다. 잠시 후 다시 시도해주세요.");
        break;
      default:
        alert(`❌ 상태 확인 실패: ${status}`);
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
      console.log("🔁 텍스트 변환 재시작 요청 성공");
    }
  } catch (error) {
    const { status, detail } = error.response?.data || {};

    switch (status) {
      case 401:
        alert("🔒 인증이 필요합니다. 다시 로그인해주세요.");
        break;
      case 404:
        alert("❗ 업로드된 음성 파일을 찾을 수 없습니다.");
        break;
      case 409:
        alert("⏳ 현재 상태에서는 재시도할 수 없습니다.");
        break;
      case 500:
        alert("⚠️ 서버 오류가 발생했습니다.");
        break;
      default:
        alert(`❌ 오류: ${status}`);
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
      console.log("🛑 변환 중단 성공");
      return;
    }

    // 204 외의 응답이 올 경우 대비 (안전망)
    throw new Error(`Unexpected response status: ${response.status}`);
  } catch (error) {
    const { status, detail } = error.response?.data || {};

    switch (status) {
      case 401:
        if (detail === "Missing token") {
          alert("🔒 인증 토큰이 없습니다. 다시 로그인해주세요.");
        } else if (detail === "Invalid token") {
          alert("🔒 유효하지 않은 토큰입니다.");
        } else if (detail === "Expired token") {
          alert("🔒 로그인 세션이 만료되었습니다.");
        }
        break;

      case 409:
        alert("⚠️ 현재 상태에서는 중단할 수 없습니다.");
        break;

      case 404:
        alert("❗ 업로드 요청이 없거나 이미 만료되었습니다.");
        break;

      case 500:
        alert("⚠️ 서버 오류가 발생했습니다. 잠시 후 다시 시도해주세요.");
        break;

      default:
        alert(`❌ 알 수 없는 오류 발생: ${status}`);
    }

    throw error;
  }
}
