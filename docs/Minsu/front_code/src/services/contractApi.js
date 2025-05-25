// src/services/contractApi.js
import api from "./apiClient";

// 계약서 생성 요청 API
export async function generateContract() {
  try {
    const response = await api.post("/contracts/generate");

    if (response.status === 202) {
      console.log("✅ 계약서 생성 요청 성공 (202 Accepted)");
      return response.data;
    }
  } catch (error) {
    if (error.response) {
      const { status, data } = error.response;

      switch (status) {
        case 401:
          if (data.detail === "Missing token") {
            alert("🔒 로그인 정보가 없습니다. 다시 로그인해주세요.");
          } else if (data.detail === "Invalid token") {
            alert("🔒 로그인 정보가 유효하지 않습니다.");
          } else if (data.detail === "Expired token") {
            alert("🔒 로그인 세션이 만료되었습니다.");
          }
          break;

        case 409:
          alert("⏳ 음성 텍스트 변환이 아직 완료되지 않았습니다.");
          break;

        case 404:
          alert("❗ 음성 파일이 업로드되지 않았거나 만료되었습니다.");
          break;

        case 500:
          alert("⚠️ 서버 오류가 발생했습니다. 잠시 후 다시 시도해주세요.");
          break;

        default:
          alert(`❗ 알 수 없는 오류: ${status}`);
      }
    } else {
      alert("❌ 네트워크 오류 또는 서버 응답 없음");
    }
    throw error;
  }
}


// 계약서 생성 상태 확인 API
export async function getContractStatus() {
  try {
    const response = await api.get("/contracts/generate/status");
    return response.data; // { status: "generating" } 또는 { status: "done", contract_id: "..." }
  } catch (error) {
    if (error.response && error.response.data && error.response.data.detail) {
      console.error("❌ 계약서 상태 확인 실패:", error.response.data.detail);
    } else {
      console.error("❌ 계약서 상태 확인 실패:", error.message || error);
    }
    throw error;
  }
}

// 계약서 생성 취소 요청 API
export async function cancelContractGeneration() {
  try {
    const response = await api.post("/contracts/generate/cancel");

    if (response.status === 204) {
      console.log("✅ 계약서 생성 프로세스 중단 성공 (204 No Content)");
    }
  } catch (error) {
    if (error.response) {
      const { status, data } = error.response;

      switch (status) {
        case 401:
          console.error("❌ 인증 실패:", data.detail);
          break;
        case 404:
          console.error("❌ 생성 요청이 없거나 만료됨:", data.detail);
          break;
        case 409:
          console.error("❌ 이미 완료되어 취소할 수 없음:", data.detail);
          break;
        case 500:
          console.error("❌ 서버 오류:", data.detail);
          break;
        default:
          console.error(`❌ 알 수 없는 오류: ${status}`);
      }
    } else {
      console.error("❌ 네트워크 오류 또는 서버 응답 없음");
    }

    throw error;
  }
}

// 전체 계약서 목록 조회
export async function getContractList() {
  const response = await api.get("/contracts");
  return response.data; // 배열 형태 반환됨
}

// 특정 계약서 상세 조회
export async function getContractContent(contractId) {
  const response = await api.get(`/contracts/${contractId}`);
  return response.data; // 응답 JSON 전체 반환
}


// 계약서 내용 수정 및 저장
export async function updateContractContent(contractId, contents) {
  const response = await api.put(`/contracts/${contractId}`, {
    contents: contents, // 전체 JSON 구조
  });
  return response.status; // 204 expected
}



// GPT 제안 텍스트 조회
export async function getSuggestions(contractId) {
  try {
    const response = await api.get(`/contracts/${contractId}/suggestions`);
    return response.data; // 예: [{ field_path: "...", suggestion_text: "..." }, ...]
  } catch (error) {
    const { status, data } = error.response || {};

    switch (status) {
      case 401:
        if (data.detail === "Missing token") {
          alert("🔒 로그인 정보가 없습니다. 다시 로그인해주세요.");
        } else if (data.detail === "Invalid token") {
          alert("🔒 로그인 정보가 유효하지 않습니다.");
        } else if (data.detail === "Expired token") {
          alert("🔒 로그인 세션이 만료되었습니다.");
        }
        break;

      case 404:
        alert("❗ 해당 계약서를 찾을 수 없습니다.");
        break;

      case 500:
        if (data.detail === "Database query failed") {
          alert("⚠️ 데이터베이스 오류가 발생했습니다.");
        } else {
          alert("⚠️ 서버 오류가 발생했습니다. 잠시 후 다시 시도해주세요.");
        }
        break;

      default:
        alert(`❌ 알 수 없는 오류: ${status}`);
    }

    throw error;
  }
}
