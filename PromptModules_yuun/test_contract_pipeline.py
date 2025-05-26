# test_contract_pipeline.py
"""
계약 처리 파이프라인 통합 테스트 모듈
"""

import json
import unittest
from unittest.mock import Mock, patch
import sys
import os

# 모듈 임포트를 위한 경로 설정
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from contract_classifier import get_contract_type
from keyword_extractor import extract_fields
from contract_annotater import annotate_contract_text

class TestContractPipeline(unittest.TestCase):
    """계약 처리 파이프라인 통합 테스트"""
    
    def setUp(self):
        """테스트 준비"""
        # Mock GPT API 응답 설정
        self.mock_gpt_caller = Mock()
        
        # 테스트용 대화 샘플
        self.sample_conversations = {
            "고용계약": """
                A: 저희 회사에서 개발자를 채용하려고 하는데, 조건을 말씀드릴게요.
                B: 네, 들어보겠습니다.
                A: 월급은 400만원이고, 주 5일 근무, 오전 9시부터 오후 6시까지입니다.
                B: 좋네요. 언제부터 시작하나요?
                A: 2024년 3월 1일부터 시작하시면 됩니다.
                B: 알겠습니다. 계약서 작성해주세요.
            """,
            "임대차계약": """
                A: 아파트 임대 조건을 말씀드릴게요.
                B: 네, 들어보겠습니다.
                A: 보증금 1억원, 월세 50만원이고, 계약기간은 2년입니다.
                B: 위치는 어디인가요?
                A: 서울시 강남구 역삼동 123번지 아파트 101호입니다.
                B: 언제부터 입주 가능한가요?
                A: 2024년 3월 1일부터 가능합니다.
            """,
            "매매계약": """
                A: 제 차를 판매하려고 합니다.
                B: 어떤 차량인가요?
                A: 2020년식 현대 소나타이고, 가격은 2000만원입니다.
                B: 상태는 어떤가요?
                A: 무사고 차량이고, 주행거리는 5만km입니다.
                B: 좋네요. 계약하겠습니다.
            """
        }

    def test_1_unit_contract_classifier(self):
        """1단계: 계약 분류기 단위 테스트"""
        print("\n=== 1단계: 계약 분류기 테스트 ===")
        
        # Mock 응답 설정
        test_cases = [
            ("증여계약", "증여"),
            ("매매계약", "매매"),
            ("교환계약", "교환"),
            ("소비대차계약", "소비대차"),
            ("사용대차계약", "사용대차"),
            ("임대차계약", "임대차"),
            ("고용계약", "고용"),
            ("도급계약", "도급")
        ]
        
        for conversation_key, expected_type in test_cases:
            with self.subTest(contract_type=expected_type):
                # Mock GPT 응답 설정
                self.mock_gpt_caller.return_value = {
                    "choices": [{"message": {"content": expected_type}}]
                }
                
                # 테스트 실행
                result = get_contract_type(
                    self.sample_conversations[conversation_key], 
                    self.mock_gpt_caller
                )
                
                print(f"입력: {conversation_key}")
                print(f"예상 결과: {expected_type}")
                print(f"실제 결과: {result}")
                print(f"테스트 결과: {'✅ PASS' if result == expected_type else '❌ FAIL'}")
                print("-" * 50)
                
                self.assertEqual(result, expected_type)

    def test_2_unit_keyword_extractor(self):
        """2단계: 키워드 추출기 단위 테스트"""
        print("\n=== 2단계: 키워드 추출기 테스트 ===")
        
        # 스키마 기반 예상 JSON 응답 모의 설정
        sample_responses = {
            "고용": {
                "employer": {
                    "company_name": "테스트 회사",
                    "representative_name": "김대표",
                    "address": "서울시 강남구 테헤란로 123",
                    "contact": "02-123-4567"
                },
                "employee": {
                    "name": "홍길동",
                    "resident_number": "901234-1******",
                    "address": "서울시 서초구 서초대로 456",
                    "contact": "010-1234-5678"
                }
            },
            "임대차": {
                "lessor": {
                    "name": "김임대"
                },
                "lessee": {
                    "name": "이세입"
                },
                "property": {
                    "address": "서울시 강남구 역삼동 123번지 아파트 101호"
                }
            }
        }
        
        for contract_type, expected_fields in sample_responses.items():
            with self.subTest(contract_type=contract_type):
                # Mock GPT 응답 설정
                self.mock_gpt_caller.return_value = Mock()
                self.mock_gpt_caller.return_value.choices = [
                    Mock(message=Mock(content=json.dumps(expected_fields, ensure_ascii=False)))
                ]
                
                # 테스트 실행
                conversation_key = f"{contract_type}계약" if contract_type != "고용" else "고용계약"
                if conversation_key in self.sample_conversations:
                    result = extract_fields(
                        self.sample_conversations[conversation_key],
                        contract_type,
                        self.mock_gpt_caller
                    )
                    
                    print(f"계약 유형: {contract_type}")
                    print(f"추출된 필드: {result}")
                    print(f"테스트 결과: {'✅ PASS' if result else '❌ FAIL'}")
                    print("-" * 50)
                    
                    self.assertIsNotNone(result)

    def test_3_unit_contract_annotater(self):
        """3단계: 계약 주석기 단위 테스트"""
        print("\n=== 3단계: 계약 주석기 테스트 ===")
        
        # 고용 계약 테스트용 필드 (일부 빈 값 포함)
        test_employment_fields = {
            "employer": {
                "company_name": "테스트 회사",
                "representative_name": "",  # 빈 값
                "address": "서울시 강남구 테헤란로 123",
                "contact": ""  # 빈 값
            },
            "employee": {
                "name": "홍길동",
                "resident_number": "",  # 빈 값
                "address": "서울시 서초구 서초대로 456",
                "contact": "010-1234-5678"
            }
        }
        
        # Mock 응답 (빈 필드에 대한 법률 검토)
        expected_employment_annotation = {
            "employer": {
                "company_name": "",
                "representative_name": "회사의 법적 대표자가 누구인지 확인하여 책임 소재를 명확히 하지 못하면 계약 이행 시 분쟁이 발생할 수 있습니다.",
                "address": "",
                "contact": "분쟁 발생 시 신속한 의사소통을 위한 필수 정보가 누락되면 문제 해결이 지연될 수 있습니다."
            },
            "employee": {
                "name": "",
                "resident_number": "근로자 신원 확인 및 4대 보험 가입 등에 필요한 정보가 누락되면 법적 의무 이행에 문제가 생길 수 있습니다.",
                "address": "",
                "contact": ""
            }
        }
        
        self.mock_gpt_caller.return_value = Mock()
        self.mock_gpt_caller.return_value.choices = [
            Mock(message=Mock(content=json.dumps(expected_employment_annotation, ensure_ascii=False)))
        ]
        
        # 고용 계약 테스트
        result = annotate_contract_text(
            "고용",
            test_employment_fields,
            self.mock_gpt_caller
        )
        
        print(f"고용 계약 입력 필드: {json.dumps(test_employment_fields, ensure_ascii=False, indent=2)}")
        print(f"고용 계약 법률 검토 결과: {json.dumps(result, ensure_ascii=False, indent=2)}")
        print(f"고용 계약 테스트 결과: {'✅ PASS' if result else '❌ FAIL'}")
        print("-" * 50)
        
        # 임대차 계약 테스트용 필드
        test_lease_fields = {
            "lessor": {
                "name": ""  # 빈 값
            },
            "lessee": {
                "name": "이세입"
            },
            "property": {
                "address": ""  # 빈 값
            }
        }
        
        expected_lease_annotation = {
            "lessor": {
                "name": "임대인의 신원 확인을 위한 필수 정보가 누락되면 계약 당사자를 특정할 수 없어 계약의 효력에 문제가 생길 수 있습니다."
            },
            "lessee": {
                "name": ""
            },
            "property": {
                "address": "임대 목적물의 위치를 명확히 하지 못하면 임대차 계약의 목적을 달성할 수 없습니다."
            }
        }
        
        self.mock_gpt_caller.return_value.choices = [
            Mock(message=Mock(content=json.dumps(expected_lease_annotation, ensure_ascii=False)))
        ]
        
        # 임대차 계약 테스트
        lease_result = annotate_contract_text(
            "임대차",
            test_lease_fields,
            self.mock_gpt_caller
        )
        
        print(f"임대차 계약 입력 필드: {json.dumps(test_lease_fields, ensure_ascii=False, indent=2)}")
        print(f"임대차 계약 법률 검토 결과: {json.dumps(lease_result, ensure_ascii=False, indent=2)}")
        print(f"임대차 계약 테스트 결과: {'✅ PASS' if lease_result else '❌ FAIL'}")
        
        self.assertIsNotNone(result)
        self.assertIsNotNone(lease_result)

    def test_4_integration_full_pipeline(self):
        """4단계: 전체 파이프라인 통합 테스트"""
        print("\n=== 4단계: 전체 파이프라인 통합 테스트 ===")
        
        for conversation_key in self.sample_conversations:
            with self.subTest(conversation=conversation_key):
                print(f"\n--- {conversation_key} 파이프라인 테스트 ---")
                
                # Step 1: 계약 분류
                expected_type = conversation_key.replace("계약", "")
                self.mock_gpt_caller.return_value = {
                    "choices": [{"message": {"content": expected_type}}]
                }
                
                contract_type = get_contract_type(
                    self.sample_conversations[conversation_key],
                    self.mock_gpt_caller
                )
                print(f"1) 계약 분류 결과: {contract_type}")
                
                # Step 2: 키워드 추출 (스키마 기반)
                if contract_type == "고용":
                    sample_fields = {
                        "employer": {
                            "company_name": "테스트 회사",
                            "representative_name": "김대표",
                            "address": "",  # 빈 값
                            "contact": "02-123-4567"
                        },
                        "employee": {
                            "name": "홍길동",
                            "resident_number": "",  # 빈 값
                            "address": "서울시 서초구 서초대로 456",
                            "contact": ""  # 빈 값
                        }
                    }
                elif contract_type == "임대차":
                    sample_fields = {
                        "lessor": {
                            "name": "김임대"
                        },
                        "lessee": {
                            "name": ""  # 빈 값
                        },
                        "property": {
                            "address": "서울시 강남구 역삼동 123번지"
                        }
                    }
                else:
                    sample_fields = {"field1": "value1", "field2": ""}
                self.mock_gpt_caller.return_value = Mock()
                self.mock_gpt_caller.return_value.choices = [
                    Mock(message=Mock(content=json.dumps(sample_fields)))
                ]
                
                extracted_fields = extract_fields(
                    self.sample_conversations[conversation_key],
                    contract_type,
                    self.mock_gpt_caller
                )
                print(f"2) 키워드 추출 결과: {extracted_fields}")
                
                # Step 3: 법률 검토 (스키마 기반)
                if contract_type == "고용":
                    annotation_result = {
                        "employer": {
                            "company_name": "",
                            "representative_name": "",
                            "address": "고용주에게 통지하거나 법적 서류를 전달할 수 있는 주소가 누락되면 법적 통지가 불가능합니다.",
                            "contact": ""
                        },
                        "employee": {
                            "name": "",
                            "resident_number": "근로자 신원 확인 및 4대 보험 가입 등에 필요한 정보가 누락되면 법적 의무 이행에 문제가 생길 수 있습니다.",
                            "address": "",
                            "contact": "계약 관련 변경 사항을 전달하기 위한 연락처가 없으면 의사소통에 문제가 생길 수 있습니다."
                        }
                    }
                elif contract_type == "임대차":
                    annotation_result = {
                        "lessor": {
                            "name": ""
                        },
                        "lessee": {
                            "name": "임차인의 신원 확인을 위한 필수 정보가 누락되면 계약 당사자를 특정할 수 없습니다."
                        },
                        "property": {
                            "address": ""
                        }
                    }
                else:
                    annotation_result = {"field1": "", "field2": "법률적 검토 의견"}
                self.mock_gpt_caller.return_value = Mock()
                self.mock_gpt_caller.return_value.choices = [
                    Mock(message=Mock(content=json.dumps(annotation_result)))
                ]
                
                final_annotation = annotate_contract_text(
                    contract_type,
                    json.loads(extracted_fields),
                    self.mock_gpt_caller
                )
                print(f"3) 법률 검토 결과: {final_annotation}")
                
                # 파이프라인 성공 여부 검증
                pipeline_success = all([
                    contract_type is not None,
                    extracted_fields is not None,
                    final_annotation is not None
                ])
                
                print(f"파이프라인 테스트 결과: {'✅ PASS' if pipeline_success else '❌ FAIL'}")
                self.assertTrue(pipeline_success)

    def test_5_error_handling(self):
        """5단계: 에러 처리 테스트"""
        print("\n=== 5단계: 에러 처리 테스트 ===")
        
        # 빈 입력 테스트
        with self.subTest("empty_input"):
            try:
                self.mock_gpt_caller.return_value = {
                    "choices": [{"message": {"content": "기타"}}]
                }
                result = get_contract_type("", self.mock_gpt_caller)
                print(f"빈 입력 처리 결과: {result}")
                self.assertIsNotNone(result)
            except Exception as e:
                print(f"빈 입력 에러: {e}")
                self.fail(f"빈 입력 처리 중 에러 발생: {e}")
        
        # 잘못된 JSON 응답 테스트
        with self.subTest("invalid_json"):
            try:
                self.mock_gpt_caller.return_value = Mock()
                self.mock_gpt_caller.return_value.choices = [
                    Mock(message=Mock(content="잘못된 JSON"))
                ]
                
                # annotate_contract_text는 JSON 파싱 실패 시 ValueError를 발생시킴
                with self.assertRaises(ValueError):
                    annotate_contract_text("고용", {}, self.mock_gpt_caller)
                print("잘못된 JSON 처리: ✅ 정상적으로 에러 처리됨")
            except Exception as e:
                print(f"JSON 에러 처리 테스트 실패: {e}")


def run_pipeline_test():
    """파이프라인 테스트 실행 함수"""
    print("=" * 60)
    print("계약 처리 파이프라인 테스트 시작")
    print("=" * 60)
    
    # 테스트 실행
    unittest.main(verbosity=2, exit=False)


if __name__ == "__main__":
    run_pipeline_test()


# ===============================
# 실제 API 연동 테스트용 별도 스크립트
# ===============================

def test_with_real_api():
    """실제 OpenAI API를 사용한 End-to-End 테스트"""
    print("\n" + "=" * 60)
    print("실제 API 연동 테스트")
    print("=" * 60)
    
    # 실제 GPT API 호출 함수
    def real_gpt_caller(messages):
        import openai
        return openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages,
            temperature=0.2
        )
    
    # 테스트용 대화
    test_conversation = """
    A: 저희 회사에서 개발자를 채용하려고 하는데요.
    B: 어떤 조건인지 말씀해주세요.
    A: 월급 500만원, 주 5일 근무, 오전 9시부터 오후 6시까지입니다.
    B: 복리후생은 어떻게 되나요?
    A: 4대보험, 연차 15일, 경조휴가 있습니다.
    B: 회사 정보를 알려주세요.
    A: 회사명은 ABC테크이고, 대표는 김철수입니다. 주소는 서울시 강남구 테헤란로 123입니다.
    B: 제 정보도 말씀드릴게요. 이름은 홍길동이고, 연락처는 010-1234-5678입니다.
    A: 언제부터 시작하나요?
    B: 2024년 4월 1일부터 시작하면 됩니다.
    """
    
    try:
        # 1단계: 계약 분류
        print("1) 계약 분류 중...")
        contract_type = get_contract_type(test_conversation, real_gpt_caller)
        print(f"계약 유형: {contract_type}")
        
        # 2단계: 키워드 추출 (실제 스키마 기반 응답 예상)
        print("\n2) 키워드 추출 중...")
        
        # 실제 추출될 것으로 예상되는 필드 구조
        expected_extracted_fields = {
            "employer": {
                "company_name": "ABC테크",
                "representative_name": "김철수", 
                "address": "서울시 강남구 테헤란로 123",
                "contact": ""  # 대화에서 누락된 정보
            },
            "employee": {
                "name": "홍길동",
                "resident_number": "",  # 대화에서 누락된 정보
                "address": "",  # 대화에서 누락된 정보
                "contact": "010-1234-5678"
            }
        }
        
        extracted_fields = extract_fields(test_conversation, contract_type, real_gpt_caller)
        print(f"추출된 필드: {json.dumps(json.loads(extracted_fields) if isinstance(extracted_fields, str) else extracted_fields, ensure_ascii=False, indent=2)}")
        
        # 3단계: 법률 검토 (누락된 필드들에 대한 검토)
        print("\n3) 법률 검토 중...")
        if isinstance(extracted_fields, str):
            try:
                fields_dict = json.loads(extracted_fields)
            except json.JSONDecodeError:
                print("키워드 추출 결과가 올바른 JSON 형식이 아닙니다.")
                return
        else:
            fields_dict = extracted_fields
            
        final_result = annotate_contract_text(contract_type, fields_dict, real_gpt_caller)
        print(f"최종 검토 결과: {json.dumps(final_result, ensure_ascii=False, indent=2)}")
        
        # 결과 분석
        print("\n📊 결과 분석:")
        print(f"- 계약 유형 분류: {contract_type}")
        print("- 추출된 주요 정보:")
        if isinstance(fields_dict, dict):
            for category, fields in fields_dict.items():
                if isinstance(fields, dict):
                    print(f"  {category}:")
                    for key, value in fields.items():
                        status = "✅ 완료" if value.strip() else "❌ 누락"
                        print(f"    - {key}: {status}")
        
        print("\n✅ 전체 파이프라인 테스트 완료!")
        
    except Exception as e:
        print(f"❌ 실제 API 테스트 실패: {e}")
        import traceback
        traceback.print_exc()


# 테스트 실행 예시
if __name__ == "__main__":
    print("1. Mock 테스트 실행")
    run_pipeline_test()
    
    print("\n" + "="*60)
    response = input("실제 API 테스트를 실행하시겠습니까? (y/n): ")
    if response.lower() == 'y':
        test_with_real_api()