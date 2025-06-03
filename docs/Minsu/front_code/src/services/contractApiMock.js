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
      console.log("✅ [Mock] 계약서 생성 요청 성공 (202)");
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
          id: "mock_employment_001",
          contract_type: "고용 계약",
          generation_status: "done",
          created_at: "2024-05-01T12:00:00Z",
          updated_at: "2024-05-02T15:30:00Z"
        },
        {
          id: "mock_sale_002",
          contract_type: "매매 계약",
          generation_status: "done",
          created_at: "2024-04-25T09:10:00Z",
          updated_at: "2024-04-25T09:20:00Z"
        },
        {
          id: "mock_construction_001",
          contract_type: "공사 계약", // 중요!
          generation_status: "done",
          created_at: "2025-05-30T11:00:00Z",
          updated_at: "2025-05-30T11:15:00Z"
        },
        {
          id: "mock_exchange_001",
          contract_type: "교환 계약", // 중요!
          generation_status: "done",
          created_at: "2025-05-31T11:00:00Z",
          updated_at: "2025-05-31T11:15:00Z"
        },
        {
          id: "mock_gift_001",
          contract_type: "증여 계약", // 중요!
          generation_status: "done",
          created_at: "2025-05-20T11:00:00Z",
          updated_at: "2025-05-20T11:15:00Z"
        },
        {
          id: "mock_lease_001",
          contract_type: "임대차 계약", // 중요!
          generation_status: "done",
          created_at: "2025-05-21T11:00:00Z",
          updated_at: "2025-05-21T11:15:00Z"
        },

        { id: "mock_loan_001",
          contract_type: "금전 대여 계약",
          generation_status: "done",
          created_at: "2024-05-03T10:00:00Z",
          updated_at: "2024-05-03T10:10:00Z" 
        },

        { id: "mock_usageloan_001",
          contract_type: "사용대차 계약",
          generation_status: "done",
          created_at: "2024-05-04T10:00:00Z",
          updated_at: "2024-05-04T10:10:00Z" 
        }
      ]);
    }, 1000); // 지연 1초
  });
}

//  /contracts/{contract_id}
// /contracts/{contract_id}
export async function getContractContent(contractId) {
  console.log("📦 Mock 계약서 요청:", contractId);

  return new Promise((resolve) => {
    setTimeout(() => {
      if (contractId === "mock_construction_001") 
        { 
          //공사계약
          resolve({
            contract_type: "공사 계약",
            contract_date: "2025-06-01",
            contractee: {
              name: "도급회사 A",
              business_number: "123-45-67890",
              address: "서울시 중구 을지로 100",
              contact: "02-1111-2222"
            },
            contractor: {
              name: "시공업체 B",
              business_number: "987-65-43210",
              address: "서울시 강남구 도산대로 200",
              contact: "02-3333-4444"
            },
            contract_details: {
              construction_name: "스마트오피스 신축 공사",
              construction_location: "서울시 송파구 법조로 55",
              construction_period: {
                start_date: "2025-07-01",
                end_date: "2025-12-31"
              },
              construction_scope: "지상 5층, 지하 2층 규모 신축",
              design_document_reference: "설계도면 2025-A1"
            },
            contract_amount: {
              total_amount: "12억 원",
              vat_included: true,
              payment_method: "계좌이체",
              payment_schedule: "착수금 30%, 중간금 40%, 준공금 30%"
            },
            obligation_and_rights: {
              ordering_party_obligation: "공사 부지 제공, 공사대금 지급",
              contractor_obligation: "공사 수행 및 일정 준수"
            },
            delay_penalty: "하루당 계약금액의 0.1%",
            warranty_period: "준공 후 1년",
            dispute_resolution: "서울중앙지방법원을 관할로 함",
            special_terms: "하자보수 보증서 제출 필요",
            signature_and_seal: "전자서명 완료"
          });
        }

      else if (contractId === "mock_employment_001") 
        {
          
          resolve({
            contract_type: "고용 계약",
            contract_date: "2025-06-15",
            employer: {
              company_name:       "주식회사 ABC",
              representative_name:"김대표",
              address:            "서울시 강남구 테헤란로 10길 20",
              contact:            "02-1234-5678"
            },
            employee: {
              name:               "홍길동",
              resident_number:    "900101-1234567",
              address:            "서울시 서초구 반포대로 50",
              contact:            "010-9876-5432"
            },
            employment_details: {
              position:           "프론트엔드 개발자",
              duties:             "React 기반 웹 앱 개발 및 유지 보수",
              workplace:          "논현동 본사 3층",
              contract_period: {
                start_date:       "2025-07-01",
                end_date:         "2026-06-30"
              },
              working_days:       "월~금",
              working_hours: {
                start_time:       "09:00",
                end_time:         "18:00",
                break_time:       "12:00~13:00"
              }
            },
            wage_details: {
              wage_type:          "월급",
              wage_amount:        "3,000,000원",
              payment_date:       "매월 25일",
              payment_method:     "계좌이체"
            },
            holidays:            "주말 및 법정공휴일",
            social_insurance: {
              national_pension:         true,
              health_insurance:         true,
              employment_insurance:     true,
              industrial_accident_insurance: true
            },
            termination:         "계약 기간 만료 30일 전 서면 통보",
            other_terms:         "퇴직금 별도 지급",
            signature_and_seal:  "전자서명 완료"
          });
        }

      else if (contractId === "mock_exchange_001") 
        {
          // 교환 계약
          resolve({contract_type: "교환 계약",
            contract_date: "2025-06-10",
            property_A: {
              location:         "서울시 종로구 세종대로 1",
              land_category:    "대지",
              land_area:        "200㎡",
              building_details: "지상 2층, 목조"
            },
            property_B: {
              location:         "서울시 강서구 김포공항로 123",
              land_category:    "임야",
              land_area:        "500㎡",
              building_details: "토지만"
            },
            party_A: {
              name:       "홍길동",
              id_number:  "900101-1234567",
              address:    "서울시 종로구 세종대로 1",
              contact:    "010-1111-2222"
            },
            party_B: {
              name:       "박영희",
              id_number:  "950505-2345678",
              address:    "서울시 강서구 김포공항로 123",
              contact:    "010-3333-4444"
            },
            exchange_payment: {
              total_price: "5억원",
              down_payment: {
                amount:       "1억원",
                payment_date: "2025-06-15"
              },
              interim_payment: {
                amount:       "2억원",
                payment_date: "2025-07-01"
              },
              balance_payment: {
                amount:       "2억원",
                payment_date: "2025-08-01"
              }
            },
            ownership_transfer: {
              document_transfer_date: "2025-09-01",
              property_delivery_date: "2025-09-05"
            },
            termination: {
              penalty_amount: "500만원"
            },
            broker: {
              office_name:         "부동산중개사무소 OO",
              office_address:      "서울시 중구 N빌딩 3층",
              representative:      "이대리",
              registration_number: "제12345호",
              broker_name:         "최중개"
            },
            special_terms:     "교환 후 1년간 재교환 금지",
            signature_and_seal: "전자서명 완료"});
        }

      else if (contractId === "mock_lease_001") 
        {
          // 임대차 계약
          resolve({
            contract_type: "임대차 계약",
            contract_date: "2025-06-20",
            property: {
              address: "서울시 마포구 독막로 100",
              land_category: "대지",
              area: "150㎡",
              building_details: "지상 3층, 철골조"
            },
            lessor: {
              name: "홍부장",
              business_number: "110-22-33333",
              address: "서울시 마포구 독막로 100",
              contact: "02-123-4567"
            },
            lessee: {
              name: "김대리",
              id_number: "921010-2345678",
              address: "서울시 마포구 독막로 102",
              contact: "010-9876-5432"
            },
            lease_amount: {
              deposit: "10,000,000원",
              rent: "월 1,000,000원",
              payment_cycle: "매월 말일"
            },
            lease_period: {
              start_date: "2025-07-01",
              end_date:   "2026-06-30"
            },
            real_estate_agent: {
              office_name:         "부동산중개사무소 장",
              office_address:      "서울시 마포구 독막로 99",
              registration_number: "제2025-123호",
              broker_name:         "박중개"
            },
            special_terms:     "임대차 종료 3개월 전 서면 통보",
            signature_and_seal:"전자서명 완료"
          });
        }

      else if (contractId === "mock_loan_001") {
        resolve({
          contract_type: "금전 대여 계약",
          contract_date: "2025-06-25",
          lender: {
            name: "한국은행",
            business_number: "000-11-22222",
            address: "서울시 중구 세종대로 39",
            contact: "02-345-6789"
          },
          borrower: {
            name: "이지원",
            resident_number: "930303-3456789",
            address: "서울시 강남구 도산대로 200",
            contact: "010-5555-6666"
          },
          loan_details: {
            amount: "20,000,000원",
            interest_rate: "연 4.5%",
            loan_term: "36개월",
            disbursement_date: "2025-07-01",
            repayment_start: "2025-08-01"
          },
          repayment_schedule: [
            { month: 1, amount: "600,000원" },
            /* … */,
            { month: 36, amount: "600,000원" }
          ],
          collateral: "없음",
          special_terms: "중도상환수수료 1% 발생",
          signature_and_seal: "전자서명 완료"
        });
      }

      else if (contractId === "mock_sale_002") 
        {
          // 매매 계약
          resolve({
             contract_type: "매매 계약",
              contract_date: "2025-06-05",
              seller: {
                name:       "홍철수",
                id_number:  "880202-1234567",
                address:    "서울시 강남구 삼성로 50",
                contact:    "02-555-1111"
              },
              buyer: {
                name:       "이영희",
                id_number:  "900303-2345678",
                address:    "서울시 송파구 올림픽로 100",
                contact:    "010-6666-2222"
              },
              property: {
                location:         "서울시 서초구 반포대로 200",
                land_category:    "대지",
                land_area:        "120㎡",
                building_details: "지상 4층, 철근콘크리트"
              },
              sale_price: {
                total_price: "5억원",
                down_payment: {
                  amount:       "1억원",
                  payment_date: "2025-06-10"
                },
                interim_payment: {
                  amount:       "2억원",
                  payment_date: "2025-07-10"
                },
                balance_payment: {
                  amount:       "2억원",
                  payment_date: "2025-08-10"
                }
              },
              ownership_transfer: {
                document_transfer_date:   "2025-09-01",
                property_delivery_date:   "2025-09-05"
              },
              termination: {
                penalty_amount: "500만원"
              },
              special_terms:     "잔금 납부 지연 시 연 5% 지연이자 발생",
              signature_and_seal: "전자서명 완료"
          });
        }

      else if (contractId === "mock_usageloan_001") 
        {
          // 사용대차 계약
          resolve({
            contract_type: "사용대차 계약",
            contract_date: "2025-06-30",
            provider: {
              name:      "오렌지렌탈㈜",
              business_number: "220-33-44444",
              address:   "서울시 동대문구 왕산로 10",
              contact:   "02-777-8888"
            },
            user: {
              name:      "박민수",
              resident_number: "920202-3456789",
              address:   "서울시 성동구 왕십리로 50",
              contact:   "010-1234-5678"
            },
            usage_object: {
              description: "고압 세척기 모델 X1000",
              serial_number: "SN-2025-00123"
            },
            usage_period: {
              start_date: "2025-07-01",
              end_date:   "2025-07-15"
            },
            special_terms:     "사용 기간 만료 후 2일 이내 반납, 연체 시 일 1만원 연체료 발생",
            signature_and_seal: "전자서명 완료"
          });
        }

      else 
        {
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
        }

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



// GPT 제안 텍스트 조회 (Mock)
export async function getSuggestions(contractId) {
  console.log("📦 [Mock] 제안 텍스트 요청:", contractId);

  return new Promise((resolve, reject) => {
// 성공 케이스
        resolve([
          {
            field_path: "gifted_property.location",
            suggestion_text: "2025년 최저임금은 시간당 10,030원입니다",
          },
          {
            field_path: "gifted_property.details.building.usage",
            suggestion_text: "점심시간은 12:00 ~ 13:00 입니다",
          },
        ]);
  });
}


export async function restoreContract(contractId) {
  console.log("📦 [Mock] 초기 계약서로 복구 요청:", contractId);

  return new Promise((resolve, reject) => {
    console.log("✅ [Mock] 복구 완료 (204)");
    resolve(); // 204 No Content
  });
}


export async function deleteContract(contractId) {
  console.log("🗑️ [Mock] 계약서 삭제 요청:", contractId);

  return new Promise((resolve, reject) => {
    console.log("✅ [Mock] 계약서 삭제 성공 (204)");
    resolve(); // 204 No Content
  });
}