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



/**
 * 음성 파일 업로드 요청 (Mock)
 * @param {string} uploadUrl
 * @param {Blob} audioBlob
 * @returns {Promise<void>}
 */
export async function uploadAudioFile(uploadUrl, audioBlob) {
  console.log("📦 [Mock] 업로드 요청:", uploadUrl);
  console.log("🎧 [Mock] 파일 크기:", audioBlob?.size, "bytes");

  return new Promise((resolve, reject) => {
    console.log("✅ [Mock] 업로드 요청 성공 (204)");
    resolve(); // 실제 204 No Content를 기대
  });
}


/**
 * 텍스트 변환 상태 조회 (Mock)
 * @returns {Promise<{ status: string }>}
 */
export async function getTranscriptionStatus() {
  const possibleStatuses = [
    "done",
  ];
  const randomStatus = possibleStatuses[Math.floor(Math.random() * possibleStatuses.length)];

  return new Promise((resolve) => {
    setTimeout(() => {
      console.log("📦 [Mock] 상태 반환:", randomStatus);
      resolve({ status: randomStatus });
    }, 1000);
  });
}


/**
 * 텍스트 변환 재시도 요청 (Mock)
 * @returns {Promise<void>}
 */
export async function retryTranscription() {
  console.log("🔁 [Mock] 변환 재시도 요청");

  return new Promise((resolve, reject) => {
    setTimeout(() => {
      const fail = Math.random() < 0.2;

      if (fail) {
        console.warn("❌ [Mock] 재시도 실패 (409)");
        reject({
          response: {
            status: 409,
            data: { detail: "Cannot retry at this stage" },
          },
        });
      } else {
        console.log("✅ [Mock] 재시도 성공 (202)");
        resolve(); // 실제는 202 Accepted
      }
    }, 1000);
  });
}



/**
 * 업로드 또는 변환 중단 요청 (Mock)
 */
export async function cancelTranscription() {
  console.log("🛑 [Mock] 중단 요청 전송");

  return new Promise((resolve, reject) => {
    setTimeout(() => {
      const failChance = Math.random();

      if (failChance < 0.2) {
        console.warn("❌ [Mock] 중단 실패 (409)");
        reject({
          response: {
            status: 409,
            data: { detail: "Cannot cancel at this stage" },
          },
        });
      } else {
        console.log("✅ [Mock] 중단 완료 (204)");
        resolve(); // 실제는 204 No Content
      }
    }, 1000);
  });
}
