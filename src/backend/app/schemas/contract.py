from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# Request Models

class ContractUpdateRequest(BaseModel):
    contents: dict

    class Config:
        schema_extra = {
            "example": {
                "contract_type": "고용",
                "contents": {
                    "contract_type": "근로계약서",
                    "employer": {"company_name": "ABC 주식회사", "representative_name": "홍길동"},
                    "employee": {"name": "김영희", "resident_number": "900101-1234567"}
                }
            }
        }


# Response Models

class ContractResponse(BaseModel):
    id: str
    contract_type: str
    created_at: datetime
    updated_at: datetime

    class Config:
        schema_extra = {
            "example": {
                "id": "contract_uuid_1",
                "contract_type": "고용",
                "created_at": "2024-05-01T12:00:00Z",
                "updated_at": "2024-05-02T15:30:00Z"
            }
        }

class ContractDetailsResponse(BaseModel):
    contract_type: str
    contents: dict
    created_at: datetime
    updated_at: datetime

    class Config:
        schema_extra = {
            "example": {
                "contract_type": "고용",
                "contents": {
                    "contract_type": "근로계약서",
                    "employer": {"company_name": "ABC 주식회사", "representative_name": "홍길동"},
                    "employee": {"name": "김영희", "resident_number": "900101-1234567"}
                },
                "created_at": "2024-05-01T12:00:00Z",
                "updated_at": "2024-05-02T15:30:00Z"
            }
        }

class GPTSuggestionResponse(BaseModel):
    field_path: str
    suggestion_text: str

    class Config:
        schema_extra = {
            "example": {
                "field_path": "wage_details.wage_amount",
                "suggestion_text": "2025년 최저임금은 시간당 10,030원입니다"
            }
        }
