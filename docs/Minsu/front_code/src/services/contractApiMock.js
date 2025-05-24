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

// /contracts
export async function getContractList() {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve([
        {
          id: "mock_contract_001",
          contract_type: "고용",
          generation_status: "done",
          created_at: "2024-05-01T12:00:00Z",
          updated_at: "2024-05-02T15:30:00Z"
        },
        {
          id: "mock_contract_002",
          contract_type: "매매",
          generation_status: "done",
          created_at: "2024-04-25T09:10:00Z",
          updated_at: "2024-04-25T09:20:00Z"
        }
      ]);
    }, 1000); // 지연 1초
  });
}

//  /contracts/{contract_id}
export async function getContractContent(contractId) {
  console.log("📦 Mock 계약서 요청:", contractId);

  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({
        contract_type: "증여 계약",
        contract_date: "2025-06-01",
        donor: {
          name: "홍길동",
          id_number: "900101-1234567",
          address: "서울시 강남구 테헤란로 123",
          contact: "010-1234-5678"
        },
        donee: {
          name: "김영희",
          id_number: "950505-2345678",
          address: "서울시 서초구 반포대로 456",
          contact: "010-2345-6789"
        },
        gifted_property: {
          type: "부동산",
          details: {
            building: {
              structure: "철근콘크리트",
              usage: "주거용",
              area: "85㎡",
              current_value: "5억 원"
            },
            land: {
              category: "대지",
              area: "100㎡",
              current_value: "3억 원"
            },
            others: "별장 포함"
          }
        },
        delivery_details: {
          delivery_date: "2025-07-01",
          delivery_method: "직접 인도"
        },
        rights_and_obligations: {
          existing_rights: "임차권 없음",
          obligations: "재산세 납부 의무"
        },
        termination_conditions: {
          reasons: "수증자의 배신행위 시",
          procedure: "서면 통보 후 14일 경과"
        },
        special_terms: "양도 후 2년간 전매 금지",
        signature_and_seal: "서명 완료"
      });
    }, 1000);
  });
}


export async function updateContractContent(contractId, contents) {
  console.log("📤 [Mock] 계약서 저장 요청:", contractId);
  console.log("📄 저장될 내용:", contents);

  return new Promise((resolve) => {
    setTimeout(() => {
      console.log("✅ [Mock] 계약서 저장 성공 (204)");
      resolve(204); // 실제 API에서 기대하는 응답 코드
    }, 1000);
  });
}

