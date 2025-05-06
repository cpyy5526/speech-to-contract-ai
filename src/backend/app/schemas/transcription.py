from pydantic import BaseModel

# Response Models

class UploadStatusResponse(BaseModel):
    status: str

    class Config:
        schema_extra = {
            "example": {
                "status": "transcribing"
            }
        }
