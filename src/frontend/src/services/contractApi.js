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
    const status = error.response?.status;
    const detail = error.response?.data?.detail || "응답 없음";

    if (status === 404) {
      if (detail === "No audio data for this user") {
        alert("❗ 음성 업로드 요청이 만료되었습니다. 다시 시도해주세요");
        window.location.href = "/";
      } else {
        alert("❗ 요청 오류: " + detail);
      }
      
    } else if (status === 409) {
      if (detail === "Transcription not ready") {
        alert("❗ 음성 업로드 또는 텍스트 변환이 완료되지 않았습니다.");
      } else {
        alert("⚠️ 게이트웨이 오류: " + detail);
      }

    } else if (status === 500) {
      if (detail === "Unexpected server error") {
        alert("⚠️ 서버 내부 오류가 발생했습니다.");
      } else {
        alert("❗ 요청 오류: " + detail);
      }

    } else {
      alert("❓ 알 수 없는 오류: " + (detail || "응답 없음"));
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
    const status = error.response?.status;
    const detail = error.response?.data?.detail || "응답 없음";

    if (status === 404) {
      if (detail === "No contract generation in progress") {
        alert("❗ 요청된 계약 생성이 없습니다. 다시 시도해주세요");
        window.location.href = "/";
      } else {
        alert("❗ 요청 오류: " + detail);
      }
      
    } else if (status === 500) {
      if (detail === "Unexpected server error") {
        alert("⚠️ 서버 내부 오류가 발생했습니다.");
      } else {
        alert("❗ 요청 오류: " + detail);
      }

    } else {
      alert("❓ 알 수 없는 오류: " + (detail || "응답 없음"));
    }

    throw error;
  }
}

// 계약서 생성 취소 요청 API
export async function cancelContractGeneration() {
  try {
    const response = await api.post("/contracts/generate/cancel");
    if (response.status === 204) return
  } catch (error) {
    const status = error.response?.status;
    const detail = error.response?.data?.detail || "응답 없음";

    if (status === 404) {
      if (detail === "No contract generation in progress") {
        alert("❗ 요청된 계약 생성이 없습니다. 다시 시도해 주세요");
        window.location.href = "/";
      } else {
        alert("❗ 요청 오류: " + detail);
      }
      
    } else if (status === 409) {
      if (detail === "Cannot cancel generation at this stage") {
        alert("❗ 취소 가능한 상태가 아닙니다.");
      } else {
        alert("⚠️ 게이트웨이 오류: " + detail);
      }

    } else if (status === 500) {
      if (detail === "Unexpected server error") {
        alert("⚠️ 서버 내부 오류가 발생했습니다.");
      } else {
        alert("❗ 요청 오류: " + detail);
      }

    } else {
      alert("❓ 알 수 없는 오류: " + (detail || "응답 없음"));
    }

    throw error;
  }
}

// 전체 계약서 목록 조회
export async function getContractList() {
  try {
    const response = await api.get("/contracts");
    return response.data; // 배열 형태 반환됨
  } catch(error){
    const status = error.response?.status;
    const detail = error.response?.data?.detail || "응답 없음";

    if (status === 500) {
      if (detail === "Database query failed") {
        alert("⚠️ 계약서 조회에 오류가 발생했습니다.");
      } else if (detail === "Unexpected server error") {
        alert("⚠️ 서버 내부 오류가 발생했습니다.");
      } else {
        alert("❗ 요청 오류: " + detail);
      }
      
    }else {
      alert("❓ 알 수 없는 오류: " + (detail || "응답 없음"));
    }

    throw error;
  }
}

// 특정 계약서 상세 조회
export async function getContractContent(contractId) {
  try {
  const response = await api.get(`/contracts/${contractId}`);
  return response.data; // 응답 JSON 전체 반환
  } catch(error){
    const status = error.response?.status;
    const detail = error.response?.data?.detail || "응답 없음";

    if (status === 404) {
      if (detail === "Contract not found") {
        alert("❗ 조회할 계약서가 존재하지 않습니다. 다시 시도해 주세요"); 
        window.location.href = "/";
      } else {
        alert("❗ 요청 오류: " + detail);
      }

    } else if (status === 500) {
      if (detail === "Database query failed") {
        alert("⚠️ 계약서 조회에 오류가 발생했습니다.");
      } else if (detail === "Unexpected server error") {
        alert("⚠️ 서버 내부 오류가 발생했습니다.");
      } else {
        alert("❗ 요청 오류: " + detail);
      }

    } else {
      alert("❓ 알 수 없는 오류: " + (detail || "응답 없음"));
    }

    throw error;
  }
}


// 계약서 내용 수정 및 저장
export async function updateContractContent(contractId, contents) {
  try{
  const response = await api.put(`/contracts/${contractId}`, {
    contents: contents, // 전체 JSON 구조
  });
  return response.status; // 204 expected
  } catch(error){
    const status = error.response?.status;
    const detail = error.response?.data?.detail || "응답 없음";

    if (status === 400) {
      if (detail === "Missing or invalid contract fields") {
        alert("❗ 수정 할 계약서 형식이 잘못되었습니다.");
      } else {
        alert("❗ 요청 오류: " + detail);
      }

    }else if (status === 404) {
      if (detail === "Contract not found") {
        alert("❗ 저장할 계약서가 존재하지 않습니다. 다시 시도해 주세요");
        window.location.href = "/";
      } else {
        alert("❗ 요청 오류: " + detail);
      }

    } else if (status === 500) {
      if (detail === "Database query failed") {
        alert("⚠️ 계약서 조회에 오류가 발생했습니다.");
      } else if (detail === "Unexpected server error") {
        alert("⚠️ 서버 내부 오류가 발생했습니다.");
      } else {
        alert("❗ 요청 오류: " + detail);
      }

    } else {
      alert("❓ 알 수 없는 오류: " + (detail || "응답 없음"));
    }

    throw error;
  }
}



// GPT 제안 텍스트 조회
export async function getSuggestions(contractId) {
  try {
    const response = await api.get(`/contracts/${contractId}/suggestions`);
    return response.data; // 예: [{ field_path: "...", suggestion_text: "..." }, ...]
  } catch(error){
    const status = error.response?.status;
    const detail = error.response?.data?.detail || "응답 없음";

    if (status === 404) {
      if (detail === "Contract not found") {
        alert("❗ 조회할 계약서가 존재하지 않습니다. 다시 시도해 주세요 ");
        window.location.href = "/";
      } else {
        alert("❗ 요청 오류: " + detail);
      }

    } else if (status === 500) {
      if (detail === "Database query failed") {
        alert("⚠️ 계약서 조회에 오류가 발생했습니다.");
      } else if (detail === "Unexpected server error") {
        alert("⚠️ 서버 내부 오류가 발생했습니다.");
      } else {
        alert("❗ 요청 오류: " + detail);
      }

    } else {
      alert("❓ 알 수 없는 오류: " + (detail || "응답 없음"));
    }

    throw error;
  }
}


// 계약서 초기 버전으로 되돌리기
export async function restoreContract(contractId) {
  try {
    const response = await api.post(`/contracts/${contractId}/restore`);
    if (response.status === 204) {
      console.log("✅ 계약서 초기 상태로 복구 성공 (204 No Content)");
    }
  } catch(error){
    const status = error.response?.status;
    const detail = error.response?.data?.detail || "응답 없음";

    if (status === 404) {
      if (detail === "Contract not found") {
        alert("❗ 복구하려는 계약서가 존재하지 않습니다. 다시 시도해 주세요 ");
        window.location.href = "/";
      } else {
        alert("❗ 요청 오류: " + detail);
      }

    } else if (status === 500) {
      if (detail === "Database query failed") {
        alert("⚠️ 계약서 조회에 오류가 발생했습니다.");
      } else if (detail === "Initial contents missing") {
        alert("⚠️ 초기 계약서 데이터를 찾지 못하였습니다.");
      } else if (detail === "Unexpected server error") {
        alert("⚠️ 서버 내부 오류가 발생했습니다.");
      } else {
        alert("❗ 요청 오류: " + detail);
      }

    } else {
      alert("❓ 알 수 없는 오류: " + (detail || "응답 없음"));
    }

    throw error;
  }
}



// 계약서 삭제
export async function deleteContract(contractId) {
  try {
    const response = await api.delete(`/contracts/${contractId}`);
    if (response.status === 204) {
      console.log("✅ 계약서 삭제 성공 (204 No Content)");
    }
  } catch(error){
    const status = error.response?.status;
    const detail = error.response?.data?.detail || "응답 없음";

    if (status === 404) {
      if (detail === "Contract not found") {
        alert("❗ 삭제할 계약서가 존재하지 않습니다. 다시 시도해 주세요 ");
        window.location.href = "/";
      } else {
        alert("❗ 요청 오류: " + detail);
      }

    } else if (status === 500) {
      if (detail === "Database query failed") {
        alert("⚠️ 계약서 조회에 오류가 발생했습니다.");
      } else if (detail === "Unexpected server error") {
        alert("⚠️ 서버 내부 오류가 발생했습니다.");
      } else {
        alert("❗ 요청 오류: " + detail);
      }

    } else {
      alert("❓ 알 수 없는 오류: " + (detail || "응답 없음"));
    }

    throw error;
  }
}
