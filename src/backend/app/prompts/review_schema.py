contract_review_schema = {
    # 8가지
    "증여": {
        "gifted_property": {
            "type": "계약의 목적물이 특정되지 않아 무효로 판단될 수 있다.",
            "details": "증여 재산이 불명확하여 계약이 무효가 될 수 있다."
        },
        "delivery_details": {
            "delivery_date": "증여 효력 발생 시점을 특정할 수 없어 분쟁이 발생할 수 있다.",
            "delivery_method": "이행 방식에 대한 다툼이 발생할 수 있다."
        },
        "rights_and_obligations": {
            "existing_rights": "권리 제한 사실로 인해 법적 충돌이 발생할 수 있다.",
            "obligations": "수증자의 책임 범위에 대한 분쟁이 발생할 수 있다."
        },
        "termination_conditions": {
            "reasons": "계약 해제 사유가 불명확해 법적 해석에 의존하게 된다.",
            "procedure": "계약 종료 절차에 대한 충돌이나 불이행 문제가 생길 수 있다."
        }
    },
    
    # 11가지
    "매매": {
        "property": {
            "location": "거래 대상 부동산이 특정되지 않아 계약의 효력 자체가 부정될 수 있다."
        },
        "sale_price": {
            "total_price": "거래 금액이 확정되지 않아 계약의 유효성이 부정되거나 분쟁이 발생할 수 있다.",
            "down_payment": {
                "amount": "계약금 지급 의무가 불분명해 이행 분쟁이 발생할 수 있다.",
                "payment_date": "계약금 지급 시점이 불분명해 계약 성립 시점 또는 효력 발생 시점에 혼란이 생길 수 있다."
            },
            "interim_payment": {
                "amount": "중도금 이행 의무가 불명확해 분쟁의 원인이 될 수 있다.",
                "payment_date": "중도금 지급 시점이 불명확해 이행기 도래 여부 판단에 혼란이 생길 수 있다."
            },
            "balance_payment": {
                "amount": "잔금 지급이 명확하지 않아 최종 이행에 장애가 생길 수 있다.",
                "payment_date": "잔금 지급 시점이 불분명해 소유권 이전 시점이나 계약 완결 시점에 법적 분쟁이 생길 수 있다."
            }
        },
        "ownership_transfer": {
            "document_transfer_date": "소유권 이전 절차가 불명확해 소유권 귀속 시점에 대한 분쟁이 발생할 수 있다.",
            "property_delivery_date": "부동산 인도 시점이 특정되지 않아 점유 이전 또는 책임 귀속에 대한 충돌이 발생할 수 있다."
        },
        "termination": {
            "penalty_amount": "계약 해제 시 손해배상 범위가 명확하지 않아 위약금 관련 분쟁이 발생할 수 있다."
        }
    },

    # 13가지
    "교환": {
        "property_A": {
            "location": "교환 대상이 특정되지 않아 계약의 효력이 부정될 수 있다."
        },
        "property_B": {
            "location": "교환 대상이 특정되지 않아 계약의 효력이 부정될 수 있다."
        },
        "exchange_payment": {
            "total_price": "차액 지급 조건이 불명확해 금전적 분쟁이 발생할 수 있다.",
            "down_payment": {
                "amount": "계약금 지급 의무가 불분명해 분쟁이 발생할 수 있다.",
                "payment_date": "계약금 지급 시점이 불분명해 계약 효력 발생 시점에 혼란이 생길 수 있다."
            },
            "interim_payment": {
                "amount": "중도금 이행 의무가 불명확해 분쟁의 원인이 될 수 있다.",
                "payment_date": "중도금 지급 시점이 불명확해 이행기 판단에 혼란이 생길 수 있다."
            },
            "balance_payment": {
                "amount": "잔금 지급이 명확하지 않아 최종 이행에 장애가 생길 수 있다.",
                "payment_date": "잔금 지급 시점이 불명확해 소유권 이전 또는 계약 완결에 법적 충돌이 발생할 수 있다."
            }
        },
        "ownership_transfer": {
            "document_transfer_date": "소유권 이전 절차가 불명확해 소유권 귀속 시점에 대한 분쟁이 발생할 수 있다.",
            "property_delivery_date": "부동산 인도 시점이 특정되지 않아 점유 이전 또는 책임 귀속에 대한 충돌이 발생할 수 있다."
        },
        "termination": {
            "penalty_amount": "계약 해제 시 손해배상 범위가 명확하지 않아 위약금 관련 분쟁이 발생할 수 있다."
        },
        "broker": {
            "office_name": "중개사무소가 없으면 중개 책임 소재가 불명확해 분쟁 시 책임 추궁이 어려울 수 있다."
        }
    },

    # 7가지
    "소비대차": {
        "loan_amount": {
            "amount_korean": "차용 금액에 대한 해석 차이가 발생할 수 있다.",
            "amount_number": "차용 금액이 특정되지 않아 계약 효력 자체가 부정될 수 있다."
        },
        "interest": {
            "rate": "이자 청구 가능 여부에 대한 분쟁이 발생할 수 있다.",
            "payment_method": "이자 지급 방식에 대한 해석 차이로 이행 분쟁이 발생할 수 있다.",
            "payment_date": "이자 지급 시점이 특정되지 않아 지연이자나 불이행 관련 분쟁이 발생할 수 있다."
        },
        "repayment": {
            "repayment_date": "원금 상환 기일이 특정되지 않아 기한 이익이나 연체 판단에 혼란이 생길 수 있다.",
            "account_info": "상환 수단이 불명확해 이행 의무의 완료 여부에 대한 분쟁이 발생할 수 있다."
        }
    },
    
    # 5가지
    "사용대차": {
        "subject_property": {
            "name": "대여 목적물이 특정되지 않아 계약 효력이 부정될 수 있다."
        },
        "loan_period": {
            "start_date": "대여 개시 시점이 불명확해 사용 권한 발생 시점에 혼란이 생길 수 있다.",
            "end_date": "반환 시점이 명확하지 않아 계약 종료나 반환 의무 이행에 분쟁이 발생할 수 있다."
        },
        "compensation_for_damage": "손해 발생 시 책임 범위에 대한 분쟁이 발생할 수 있다.",
        "restoration_obligation": "원상복구 의무 여부가 불분명해 반환 시 분쟁이 발생할 수 있다."
    },

    # 10가지
    "임대차": {
        "property": {
            "address": "임대 대상이 특정되지 않아 계약 효력이 부정될 수 있다."
        },
        "lease_terms": {
            "deposit": "보증금 금액이 명확하지 않아 반환 의무나 분쟁 발생 시 기준이 모호해질 수 있다.",
            "monthly_rent": "임대료가 확정되지 않아 지급 의무 불이행 여부 판단에 혼란이 생길 수 있다.",
            "contract_period": {
                "start_date": "임대 개시 시점이 불분명해 사용 권한 발생 시점에 혼란이 생길 수 있다.",
                "end_date": "임대 종료 시점이 불명확해 계약 갱신, 퇴거, 보증금 반환 시점에 분쟁이 발생할 수 있다."
            },
            "payment_date": "임대료 지급일이 명확하지 않아 연체나 계약 해지 사유에 대한 판단이 어려워질 수 있다."
        },
        "management_fee": "관리비 부담 주체나 금액이 불명확해 분쟁이 발생할 수 있다.",
        "delivery_date": "인도 시점이 명확하지 않아 사용개시 시점이나 손해 발생 책임에 대한 다툼이 발생할 수 있다.",
        "termination": "계약 해지 사유가 불명확해 일방 해제 시 분쟁이 발생할 수 있다.",
        "real_estate_agent": {
            "office_name": "중개사무소가 없으면 중개 책임 소재가 불명확해 분쟁 시 책임 추궁이 어려울 수 있다.",
        }
    },
    
    # 12가지
    "고용": {
        "employment_details": {
            "duties": "업무 내용이 구체화되지 않아 업무 범위나 평가 기준에 대한 분쟁이 발생할 수 있다.",
            "workplace": "근무 장소가 불명확해 근로 장소 변경이나 통근 비용 등에서 분쟁이 생길 수 있다.",
            "contract_period": {
                "start_date": "근로 개시일이 특정되지 않아 계약 효력 발생 시점에 혼란이 생길 수 있다.",
                "end_date": "종료일이 없으면 기간제 여부가 불명확해 해고 제한 규정 적용에 혼란이 생길 수 있다."
            },
            "working_days": "근로일이 명확하지 않아 휴일, 연차 계산 및 소정근로시간 판단에 문제가 생길 수 있다.",
            "working_hours": {
                "start_time": "근무 시작 시간이 명확하지 않아 초과근로 판단에 문제가 생길 수 있다.",
                "end_time": "근무 종료 시간이 불분명해 근로시간 산정과 임금 계산에 분쟁이 생길 수 있다."
            }
        },
        "wage_details": {
            "wage_type": "급여 형태가 명확하지 않아 임금 계산 방식에 혼란이 생길 수 있다.",
            "wage_amount": "급여 금액이 특정되지 않아 임금 미지급 또는 체불에 대한 분쟁이 발생할 수 있다.",
            "payment_date": "임금 지급일이 없으면 지연지급이나 체불 발생 시 책임 판단이 어려워질 수 있다.",
            "payment_method": "지급 방식이 명확하지 않아 이체 오류나 지급 이행 여부에 대한 분쟁이 생길 수 있다."
        },
        "termination": "해지 조건이 명확하지 않아 해고나 계약 종료 시 부당 해고 논란이 발생할 수 있다."
    },
    
    # 13가지
    "도급": {
        "contract_details": {
            "construction_name": "공사 명칭이 명확하지 않아 계약 대상이 특정되지 않을 수 있다.",
            "construction_location": "공사 위치가 불분명해 이행 장소 및 책임 소재에 혼란이 생길 수 있다.",
            "construction_period": {
                "start_date": "공사 시작일이 특정되지 않아 계약 이행 개시 시점에 대한 분쟁이 발생할 수 있다.",
                "end_date": "공사 완료일이 명확하지 않아 지연 여부 판단 및 지체상금 산정에 문제가 생길 수 있다."
            },
            "construction_scope": "공사 범위가 명확하지 않아 책임 범위나 추가 비용 발생 여부에 대한 분쟁이 발생할 수 있다."
        },
        "contract_amount": {
            "total_amount": "계약 금액이 특정되지 않아 대금 지급 의무나 범위에 대한 분쟁이 생길 수 있다.",
            "payment_method": "지급 방식이 불명확해 이행 여부나 지연 책임에 대한 다툼이 발생할 수 있다.",
            "payment_schedule": "지급 일정이 명확하지 않아 각 회차별 지급 시점 또는 지연 판단에 문제가 생길 수 있다."
        },
        "obligation_and_rights": {
            "ordering_party_obligation": "도급인의 의무가 명확하지 않아 현장 제공, 자재 지급 등 이행 충돌이 발생할 수 있다.",
            "contractor_obligation": "수급인의 이행 책임이 명확하지 않아 공사 불이행이나 하자 발생 시 분쟁이 발생할 수 있다."
        },
        "delay_penalty": "지연 위약금 조건이 없으면 공사 지연 시 손해배상 기준이 없어 분쟁이 발생할 수 있다.",
        "warranty_period": "하자보수 기간이 정해지지 않으면 하자 발생 시 보수 책임 범위에 대한 분쟁이 생길 수 있다.",
        "dispute_resolution": "분쟁 해결 절차가 명시되지 않으면 분쟁 발생 시 관할이나 절차에 대한 충돌이 발생할 수 있다."
    }

}
