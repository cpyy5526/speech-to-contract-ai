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

class UploadInitResponse(BaseModel):
    upload_url: str

    class Config:
        schema_extra = {
            "example": {
                "upload_url": "https://upload.myservice.com/upload/audio/abc123-def456-uuid"
            }
        }