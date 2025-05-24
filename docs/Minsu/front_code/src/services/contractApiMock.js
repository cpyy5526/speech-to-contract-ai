// src/services/contractApi.js
import api from "./apiClient";


// /contracts/generate
export async function generateContract() {
  const errorCases = [
    { status: 401, detail: "Missing token" },
    { status: 401, detail: "Invalid token" },
    { status: 409, detail: "Transcription not ready" },
    { status: 404, detail: "No audio data for this user" },
    { status: 500, detail: "Unexpected server error" },
  ];

  const random = errorCases[Math.floor(Math.random() * errorCases.length)];

//   실패 테스트용 코드
//   return new Promise((_, reject) => {
//     setTimeout(() => {
//       reject({
//         response: {
//           status: random.status,
//           data: { detail: random.detail },
//         },
//       });
//     }, 1000);
//   });

  return new Promise((resolve) => {
    setTimeout(() => {
      console.log("✅ [Mock] 계약서 생성 성공 (202)");
      resolve({ message: "Contract generation started" }); // 필요 시 데이터 반환
    }, 1000);
  });

}


// /contracts/generate/status
export async function getContractStatus() {
  const possibleStates = ["generating", "done", "failed", "cancelled"];
  const random = possibleStates[Math.floor(Math.random() * possibleStates.length)];

  return new Promise((resolve) => {
    setTimeout(() => {
      if (random === "done") {
        resolve({ status: "done", contract_id: "mock_contract_id_123" });
      } else {
        resolve({ status: random }); // failed도 포함해서 resolve
      }
    }, 1000);
  });
}

// /contracts/generate/cancel
export async function cancelContractGeneration() {
  console.log("⚠️ [Mock] 계약서 생성 취소 요청");

  return new Promise((resolve, reject) => {
    setTimeout(() => {
      // 랜덤으로 성공/실패 시뮬레이션
      const shouldFail = Math.random() < 0.2; // 20% 확률로 실패

      if (shouldFail) {
        reject({
          response: {
            status: 409,
            data: {
              detail: "이미 완료되어 취소할 수 없습니다.",
            },
          },
        });
      } else {
        console.log("✅ [Mock] 계약서 생성 취소 완료 (204)");
        resolve(); // 실제 API는 204 No Content 반환
      }
    }, 1000);
  });
}

