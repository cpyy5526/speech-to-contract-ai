keyword_schema = {
    "증여": {
        "contract_type": "계약의 종류를 구분하는 항목. 증여 여부를 나타냄.",

        "gifted_property": {
            "type": {"description": "증여 재산의 종류를 나타내는 항목. 부동산, 동산, 기타로 구분."},
            "details": {
                "description": "증여 재산의 구체적인 내용을 나타내는 항목.",
                "area": "재산의 면적이나 크기를 나타내는 항목.",
                "current_value": "재산의 시가 또는 평가 금액을 나타내는 항목."
            }
        },

        "delivery_details": {
            "delivery_date": "재산 이전 날짜를 나타내는 항목. 반드시 'YYYY-MM-DD' 형식의 확정된 날짜로 기입하며, 상대적 표현은 허용하지 않습니다.",
            "delivery_method": "재산을 이전하는 방식을 나타내는 항목."
        },

        "rights_and_obligations": {
            "existing_rights": "증여 재산에 설정된 기존 권리를 나타내는 항목.",
            "obligations": "수증자가 부담하는 의무나 책임을 나타내는 항목."
        },

        "termination_conditions": {
            "reasons": "계약 해제 또는 종료 사유를 나타내는 항목.",
            "procedure": "계약 해제 시 절차나 방식을 나타내는 항목."
        },

        "special_terms": "계약서에 포함되는 특약사항을 자연어 문장으로 정리하는 항목입니다.",

        "donor": {
            "name": "증여자의 성명을 나타내는 항목.",
            "id_number": "증여자의 주민등록번호 또는 식별번호를 나타내는 항목.",
            "address": "증여자의 주소를 나타내는 항목.",
            "contact": "증여자의 연락처를 나타내는 항목."
        },

        "donee": {
            "name": "수증자의 성명을 나타내는 항목.",
            "id_number": "수증자의 주민등록번호 또는 식별번호를 나타내는 항목.",
            "address": "수증자의 주소를 나타내는 항목.",
            "contact": "수증자의 연락처를 나타내는 항목."
        },

        "contract_date": "계약 체결 일자를 나타내는 항목. 반드시 'YYYY-MM-DD' 형식의 확정된 날짜로 기입하며, 상대적 표현은 허용하지 않습니다.",
        "signature_and_seal": "계약 당사자의 서명 또는 날인 여부를 나타내는 항목."
    },

    "매매": {
        "contract_type": "계약의 종류를 구분하는 항목. 매매 여부를 나타냄.",

        "property": {
            "location": "거래 대상 부동산의 위치를 나타내는 항목.",
            "land_category": "토지의 지목을 나타내는 항목.",
            "land_area": "토지의 면적을 나타내는 항목.",
            "building_details": "건물의 구조, 용도, 면적 등 구체적인 내용을 나타내는 항목."
        },

        "seller": {
            "name": "매도인의 성명을 나타내는 항목.",
            "id_number": "매도인의 주민등록번호 또는 식별번호를 나타내는 항목.",
            "address": "매도인의 주소를 나타내는 항목.",
            "contact": "매도인의 연락처를 나타내는 항목."
        },

        "buyer": {
            "name": "매수인의 성명을 나타내는 항목.",
            "id_number": "매수인의 주민등록번호 또는 식별번호를 나타내는 항목.",
            "address": "매수인의 주소를 나타내는 항목.",
            "contact": "매수인의 연락처를 나타내는 항목."
        },

        "sale_price": {
            "total_price": "부동산 매매의 총 거래금액을 나타내는 항목.",
            "down_payment": {
                "amount": "계약금의 금액을 나타내는 항목.",
                "payment_date": "계약금 지급 일자를 나타내는 항목. 반드시 'YYYY-MM-DD' 형식의 확정된 날짜로 기입하며, 상대적 표현은 허용하지 않습니다."
            },
            "interim_payment": {
                "amount": "중도금의 금액을 나타내는 항목.",
                "payment_date": "중도금 지급 일자를 나타내는 항목. 반드시 'YYYY-MM-DD' 형식의 확정된 날짜로 기입하며, 상대적 표현은 허용하지 않습니다."
            },
            "balance_payment": {
                "amount": "잔금의 금액을 나타내는 항목.",
                "payment_date": "잔금 지급 일자를 나타내는 항목. 반드시 'YYYY-MM-DD' 형식의 확정된 날짜로 기입하며, 상대적 표현은 허용하지 않습니다."
            }
        },

        "ownership_transfer": {
            "document_transfer_date": "소유권 이전을 위한 서류 이전 일자를 나타내는 항목. 반드시 'YYYY-MM-DD' 형식의 확정된 날짜로 기입하며, 상대적 표현은 허용하지 않습니다.",
            "property_delivery_date": "부동산 인도 일자를 나타내는 항목. 반드시 'YYYY-MM-DD' 형식의 확정된 날짜로 기입하며, 상대적 표현은 허용하지 않습니다."
        },

        "termination": {
            "penalty_amount": "계약 해제 시 발생하는 위약금 금액을 나타내는 항목."
        },

        "special_terms": "계약서에 포함되는 특약사항을 자연어 문장으로 정리하는 항목입니다.",

        "contract_date": "계약 체결 일자를 나타내는 항목. 반드시 'YYYY-MM-DD' 형식의 확정된 날짜로 기입하며, 상대적 표현은 허용하지 않습니다.",
        "signature_and_seal": "계약 당사자의 서명 또는 날인 여부를 나타내는 항목."
    },

    "교환": {
        "contract_type": "계약의 종류를 구분하는 항목. 교환 여부를 나타냄.",

        "property_A": {
            "location": "갑 부동산의 위치를 나타내는 항목.",
            "land_category": "갑 부동산의 토지 지목을 나타내는 항목.",
            "land_area": "갑 부동산의 면적을 나타내는 항목.",
            "building_details": "갑 부동산의 건물 구조, 용도, 면적 등 구체적인 내용을 나타내는 항목."
        },

        "property_B": {
            "location": "을 부동산의 위치를 나타내는 항목.",
            "land_category": "을 부동산의 토지 지목을 나타내는 항목.",
            "land_area": "을 부동산의 면적을 나타내는 항목.",
            "building_details": "을 부동산의 건물 구조, 용도, 면적 등 구체적인 내용을 나타내는 항목."
        },

        "party_A": {
            "name": "갑 당사자의 성명을 나타내는 항목.",
            "id_number": "갑 당사자의 주민등록번호 또는 식별번호를 나타내는 항목.",
            "address": "갑 당사자의 주소를 나타내는 항목.",
            "contact": "갑 당사자의 연락처를 나타내는 항목."
        },

        "party_B": {
            "name": "을 당사자의 성명을 나타내는 항목.",
            "id_number": "을 당사자의 주민등록번호 또는 식별번호를 나타내는 항목.",
            "address": "을 당사자의 주소를 나타내는 항목.",
            "contact": "을 당사자의 연락처를 나타내는 항목."
        },

        "exchange_payment": {
            "total_price": "교환에 따른 차액 지급 총액을 나타내는 항목.",
            "down_payment": {
                "amount": "계약금의 금액을 나타내는 항목.",
                "payment_date": "계약금 지급 일자를 나타내는 항목. 반드시 'YYYY-MM-DD' 형식의 확정된 날짜로 기입하며, 상대적 표현은 허용하지 않습니다."
            },
            "interim_payment": {
                "amount": "중도금의 금액을 나타내는 항목.",
                "payment_date": "중도금 지급 일자를 나타내는 항목. 반드시 'YYYY-MM-DD' 형식의 확정된 날짜로 기입하며, 상대적 표현은 허용하지 않습니다."
            },
            "balance_payment": {
                "amount": "잔금의 금액을 나타내는 항목.",
                "payment_date": "잔금 지급 일자를 나타내는 항목. 반드시 'YYYY-MM-DD' 형식의 확정된 날짜로 기입하며, 상대적 표현은 허용하지 않습니다."
            }
        },

        "ownership_transfer": {
            "document_transfer_date": "소유권 이전 서류 전달 일자를 나타내는 항목. 반드시 'YYYY-MM-DD' 형식의 확정된 날짜로 기입하며, 상대적 표현은 허용하지 않습니다.",
            "property_delivery_date": "부동산 인도 일자를 나타내는 항목. 반드시 'YYYY-MM-DD' 형식의 확정된 날짜로 기입하며, 상대적 표현은 허용하지 않습니다."
        },

        "termination": {
            "penalty_amount": "계약 해제 시 발생하는 위약금 금액을 나타내는 항목."
        },

        "special_terms": "계약서에 포함되는 특약사항을 자연어 문장으로 정리하는 항목입니다.",

        "broker": {
            "office_address": "중개사무소의 주소를 나타내는 항목.",
            "office_name": "중개사무소의 명칭을 나타내는 항목.",
            "representative": "중개사무소 대표자의 성명을 나타내는 항목.",
            "registration_number": "중개사무소의 등록번호를 나타내는 항목.",
            "broker_name": "거래를 담당한 중개사의 성명을 나타내는 항목."
        },

        "contract_date": "계약 체결 일자를 나타내는 항목. 반드시 'YYYY-MM-DD' 형식의 확정된 날짜로 기입하며, 상대적 표현은 허용하지 않습니다.",
        "signature_and_seal": "계약 당사자의 서명 또는 날인 여부를 나타내는 항목."
    },

    "소비대차": {
        "contract_type": "계약의 종류를 구분하는 항목. 금전소비대차 여부를 나타냄.",

        "loan_amount": {
            "amount_korean": "금액을 한글로 표기한 항목.",
            "amount_number": "금액을 숫자로 표기한 항목."
        },

        "creditor": {
            "name": "채권자의 성명을 나타내는 항목.",
            "id_number": "채권자의 주민등록번호 또는 식별번호를 나타내는 항목.",
            "address": "채권자의 주소를 나타내는 항목.",
            "contact": "채권자의 연락처를 나타내는 항목."
        },

        "debtor": {
            "name": "채무자의 성명을 나타내는 항목.",
            "id_number": "채무자의 주민등록번호 또는 식별번호를 나타내는 항목.",
            "address": "채무자의 주소를 나타내는 항목.",
            "contact": "채무자의 연락처를 나타내는 항목."
        },

        "interest": {
            "rate": "이자율을 나타내는 항목.",
            "payment_method": "이자 지급 방식을 나타내는 항목.",
            "payment_date": "이자 지급 일자를 나타내는 항목. 반드시 'YYYY-MM-DD' 형식의 확정된 날짜로 기입하며, 상대적 표현은 허용하지 않습니다."
        },

        "repayment": {
            "repayment_date": "원금 상환 일자를 나타내는 항목. 반드시 'YYYY-MM-DD' 형식의 확정된 날짜로 기입하며, 상대적 표현은 허용하지 않습니다.",
            "repayment_method": "원금 상환 방식을 나타내는 항목.",
            "repayment_location": "원금 상환 장소를 나타내는 항목.",
            "account_info": "원금 상환 계좌 정보를 나타내는 항목."
        },

        "special_terms": "계약서에 포함되는 특약사항을 자연어 문장으로 정리하는 항목입니다.",

        "contract_date": "계약 체결 일자를 나타내는 항목. 반드시 'YYYY-MM-DD' 형식의 확정된 날짜로 기입하며, 상대적 표현은 허용하지 않습니다.",
        "signature_and_seal": "계약 당사자의 서명 또는 날인 여부를 나타내는 항목."
    },
    
    "사용대차": {
        "contract_type": "계약의 종류를 구분하는 항목. 사용대차 여부를 나타냄.",

        "lender": {
            "name": "대여인의 성명을 나타내는 항목.",
            "address": "대여인의 주소를 나타내는 항목."
        },

        "borrower": {
            "name": "차용인의 성명을 나타내는 항목.",
            "address": "차용인의 주소를 나타내는 항목."
        },

        "subject_property": {
            "name": "대여된 목적물의 명칭을 나타내는 항목."
        },

        "loan_period": {
            "start_date": "대여 시작일을 나타내는 항목. 반드시 'YYYY-MM-DD' 형식의 확정된 날짜로 기입하며, 상대적 표현은 허용하지 않습니다.",
            "end_date": "대여 종료일을 나타내는 항목. 반드시 'YYYY-MM-DD' 형식의 확정된 날짜로 기입하며, 상대적 표현은 허용하지 않습니다."
        },

        "purpose_of_use": "대여 목적물의 사용 목적을 나타내는 항목.",
        "compensation_for_damage": "손해 발생 시 배상 조건을 나타내는 항목.",
        "restoration_obligation": "반환 시 원상복구 의무 관련 내용을 나타내는 항목.",

        "contract_date": "계약 체결 일자를 나타내는 항목. 반드시 'YYYY-MM-DD' 형식의 확정된 날짜로 기입하며, 상대적 표현은 허용하지 않습니다.",
        "signature_and_seal": "계약 당사자의 서명 또는 날인 여부를 나타내는 항목."
    },

    "임대차": {
        "contract_type": "계약의 종류를 구분하는 항목. 임대차 여부를 나타냄.",

        "property": {
            "address": "임대 대상 부동산의 주소를 나타내는 항목.",
            "land_category": "토지의 지목을 나타내는 항목.",
            "area": "부동산의 면적을 나타내는 항목.",
            "building_details": "건물의 구조, 용도, 층수 등 구체적인 정보를 나타내는 항목."
        },

        "lessor": {
            "name": "임대인의 성명을 나타내는 항목.",
            "resident_number": "임대인의 주민등록번호 또는 식별번호를 나타내는 항목.",
            "address": "임대인의 주소를 나타내는 항목.",
            "contact": "임대인의 연락처를 나타내는 항목."
        },

        "lessee": {
            "name": "임차인의 성명을 나타내는 항목.",
            "resident_number": "임차인의 주민등록번호 또는 식별번호를 나타내는 항목.",
            "address": "임차인의 주소를 나타내는 항목.",
            "contact": "임차인의 연락처를 나타내는 항목."
        },

        "lease_terms": {
            "deposit": "임대차 계약의 보증금을 나타내는 항목.",
            "monthly_rent": "월세 금액을 나타내는 항목.",
            "contract_period": {
                "start_date": "임대차 시작일을 나타내는 항목. 반드시 'YYYY-MM-DD' 형식의 확정된 날짜로 기입하며, 상대적 표현은 허용하지 않습니다.",
                "end_date": "임대차 종료일을 나타내는 항목. 반드시 'YYYY-MM-DD' 형식의 확정된 날짜로 기입하며, 상대적 표현은 허용하지 않습니다."
            },
            "payment_date": "임대료 지급일을 나타내는 항목. 반드시 'YYYY-MM-DD' 형식의 확정된 날짜로 기입하며, 상대적 표현은 허용하지 않습니다."
        },

        "management_fee": "관리비 항목 또는 금액을 나타내는 항목.",
        "use_purpose": "임대 목적물의 사용 목적을 나타내는 항목.",
        "delivery_date": "부동산의 인도 일자를 나타내는 항목. 반드시 'YYYY-MM-DD' 형식의 확정된 날짜로 기입하며, 상대적 표현은 허용하지 않습니다.",
        "termination": "계약 해지 사유나 조건을 서술하는 항목.",
        "special_terms": "계약서에 포함되는 특약사항을 자연어 문장으로 정리하는 항목입니다.",

        "real_estate_agent": {
            "office_address": "중개사무소의 주소를 나타내는 항목.",
            "office_name": "중개사무소의 명칭을 나타내는 항목.",
            "representative_name": "중개사무소 대표자의 이름을 나타내는 항목.",
            "registration_number": "중개사무소의 등록번호를 나타내는 항목.",
            "broker_name": "거래를 중개한 공인중개사의 이름을 나타내는 항목."
        },

        "contract_date": "계약 체결 일자를 나타내는 항목. 반드시 'YYYY-MM-DD' 형식의 확정된 날짜로 기입하며, 상대적 표현은 허용하지 않습니다.",
        "signature_and_seal": "계약 당사자의 서명 또는 날인 여부를 나타내는 항목."
    },
    
    "고용": {
        "contract_type": "계약의 종류를 구분하는 항목. 근로계약 여부를 나타냄.",

        "employer": {
            "company_name": "사용자(회사)의 상호명을 나타내는 항목.",
            "representative_name": "대표자의 이름을 나타내는 항목.",
            "address": "회사의 주소를 나타내는 항목.",
            "contact": "회사의 전화번호 등 연락처를 나타내는 항목."
        },

        "employee": {
            "name": "근로자의 성명을 나타내는 항목.",
            "resident_number": "근로자의 주민등록번호 또는 식별번호를 나타내는 항목.",
            "address": "근로자의 주소를 나타내는 항목.",
            "contact": "근로자의 연락처를 나타내는 항목."
        },

        "employment_details": {
            "position": "근로자의 직위를 나타내는 항목.",
            "duties": "근로자의 담당 업무를 나타내는 항목.",
            "workplace": "근로 장소를 나타내는 항목.",
            "contract_period": {
                "start_date": "근로계약 시작일. 반드시 'YYYY-MM-DD' 형식의 확정된 날짜로 기입하며, 상대적 표현은 허용하지 않습니다.",
                "end_date": "근로계약 종료일. 반드시 'YYYY-MM-DD' 형식의 확정된 날짜로 기입하며, 상대적 표현은 허용하지 않습니다."
            },
            "working_days": "근무 요일 또는 주당 근무 일수를 나타내는 항목.",
            "working_hours": {
                "start_time": "근무 시작 시간을 나타내는 항목.",
                "end_time": "근무 종료 시간을 나타내는 항목.",
                "break_time": "휴게 시간을 나타내는 항목."
            }
        },

        "wage_details": {
            "wage_type": "급여 형태(시급, 월급 등)를 나타내는 항목.",
            "wage_amount": "지급 급여 금액을 나타내는 항목.",
            "allowances": "각종 수당(교통비, 식비, 야근수당, 초과근무수당 등)과 추가 급여를 나타내는 항목. 금액과 지급 조건을 포함한 모든 수당과 상여 관련 내용을 기록.",
            "payment_date": "임금 지급일을 나타내는 항목. 반드시 'YYYY-MM-DD' 형식의 확정된 날짜로 기입하며, 상대적 표현은 허용하지 않습니다.",
            "payment_method": "임금 지급 방법(계좌이체 등)을 나타내는 항목."
        },

        "holidays": "유급휴일 또는 정기휴일에 대한 내용을 나타내는 항목.",

        "social_insurance": {
            "national_pension": "국민연금 가입 여부를 나타내는 항목.",
            "health_insurance": "건강보험 가입 여부를 나타내는 항목.",
            "employment_insurance": "고용보험 가입 여부를 나타내는 항목.",
            "industrial_accident_insurance": "산재보험 가입 여부를 나타내는 항목."
        },

        "termination": "근로계약 해지 조건 또는 절차를 나타내는 항목.",
        "other_terms": "계약서에 포함되는 기타 조건을 자연어 문장으로 정리하는 항목입니다.",
        "contract_date": "근로계약 체결일. 반드시 'YYYY-MM-DD' 형식의 확정된 날짜로 기입하며, 상대적 표현은 허용하지 않습니다.",
        "signature_and_seal": "계약 당사자의 서명 또는 날인 여부를 나타내는 항목."
    },
    
    "도급": {
        "contract_type": "계약의 종류를 구분하는 항목. 도급계약 여부를 나타냄.",

        "contractee": {
            "name": "도급인(주문자)의 이름 또는 상호를 나타내는 항목.",
            "business_number": "도급인의 사업자등록번호를 나타내는 항목.",
            "address": "도급인의 주소를 나타내는 항목.",
            "contact": "도급인의 연락처를 나타내는 항목."
        },

        "contractor": {
            "name": "수급인(시공자)의 이름 또는 상호를 나타내는 항목.",
            "business_number": "수급인의 사업자등록번호를 나타내는 항목.",
            "address": "수급인의 주소를 나타내는 항목.",
            "contact": "수급인의 연락처를 나타내는 항목."
        },

        "contract_details": {
            "construction_name": "공사의 명칭을 나타내는 항목.",
            "construction_location": "공사 위치 또는 현장을 나타내는 항목.",
            "construction_period": {
                "start_date": "공사 시작일을 나타내는 항목. 반드시 'YYYY-MM-DD' 형식의 확정된 날짜로 기입하며, 상대적 표현은 허용하지 않습니다.",
                "end_date": "공사 완료일을 나타내는 항목. 반드시 'YYYY-MM-DD' 형식의 확정된 날짜로 기입하며, 상대적 표현은 허용하지 않습니다."
            },
            "construction_scope": "공사의 범위 및 내용을 설명하는 항목.",
            "design_document_reference": "설계 도서, 사양서 등 참고 문서의 명칭 또는 번호를 기재하는 항목."
        },

        "contract_amount": {
            "total_amount": "공사 계약 총액을 나타내는 항목.",
            "vat_included": "부가가치세 포함 여부를 나타내는 항목.",
            "payment_method": "공사대금의 지급 방법을 나타내는 항목.",
            "payment_schedule": "공사대금 지급 일정이나 회차 등을 나타내는 항목."
        },

        "obligation_and_rights": {
            "ordering_party_obligation": "도급인의 주요 의무 사항을 나타내는 항목.",
            "contractor_obligation": "수급인의 주요 의무 사항을 나타내는 항목."
        },

        "delay_penalty": "공사 지연 시 위약금 또는 지체상금 조건을 나타내는 항목.",
        "warranty_period": "하자보수 또는 품질보증 기간을 나타내는 항목.",
        "dispute_resolution": "분쟁 발생 시 해결 절차 또는 기관을 나타내는 항목.",
        "special_terms": "계약서에 포함되는 특약사항을 자연어 문장으로 정리하는 항목입니다.",
        "contract_date": "계약 체결 일자를 나타내는 항목. 반드시 'YYYY-MM-DD' 형식의 확정된 날짜로 기입하며, 상대적 표현은 허용하지 않습니다.",
        "signature_and_seal": "계약 당사자의 서명 또는 날인 여부를 나타내는 항목."
    },
    
    "기타": {
        "description": "대화 내용을 바탕으로 전체 계약 내용을 자연어로 정리한 텍스트를 작성하는 항목입니다."
    }
}


