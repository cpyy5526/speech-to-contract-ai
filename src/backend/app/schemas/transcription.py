from pydantic import BaseModel

# Request Models

class UploadInitRequest(BaseModel):
    filename: str

    class Config:
        schema_extra = {
            "example": {
                "filename": "recording.wav"
            }
        }


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
    '''
    # ========================= 실제 배포용 (시작) ========================
    upload_url: str

    class Config:
        schema_extra = {
            "example": {
                "upload_url": "https://upload.myservice.com/upload/audio/abc123-def456-uuid"
            }
        }
    # ========================= 실제 배포용(끝) =========================
    '''

    # ========================= 사내 시연용 (시작) ========================
    internal_upload_url: str
    external_upload_url: str

    class Config:
        schema_extra = {
            "example": {
                "internal_upload_url": "http://192.168.0.49:8080/upload/audio/abc123-def456-uuid",
                "external_upload_url": "https://xxxx.ngrok-free.app/upload/audio/abc123-def456-uuid"
            }
        }
    # ========================= 사내 시연용 (끝) =========================