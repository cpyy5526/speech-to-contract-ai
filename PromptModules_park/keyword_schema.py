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

    "기타": {
        "description": "대화 내용을 바탕으로 전체 계약 내용을 자연어로 정리한 텍스트를 작성하는 항목입니다."
    }
}


