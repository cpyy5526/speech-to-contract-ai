from pydantic import BaseModel
from typing import Optional

# Response Models

class GenerationStatusResponse(BaseModel):
    status: str
    contract_id: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "status": "generating"
            }
        }
