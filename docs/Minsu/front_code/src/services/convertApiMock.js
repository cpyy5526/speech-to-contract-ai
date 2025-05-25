import api from "./apiClient";

// services/convertApiMock.js

/**
 * 음성 업로드 예약 요청 (Mock)
 * @param {string} filename
 * @returns {Promise<string>} pre-signed upload URL
 */
export async function initiateTranscription(filename) {
  console.log("📦 [Mock] initiateTranscription 호출됨:", filename);

  return new Promise((resolve, reject) => {
    setTimeout(() => {
      // 실패 케이스 랜덤으로 섞을 수도 있음 (여기선 성공만 처리)
      const mockUploadUrl = `https://mock-upload-url.com/upload/${filename}`;
      console.log("✅ [Mock] 업로드 URL 발급 완료:", mockUploadUrl);
      resolve({ upload_url: mockUploadUrl });
    }, 1000); // 1초 지연
  });
}
