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
