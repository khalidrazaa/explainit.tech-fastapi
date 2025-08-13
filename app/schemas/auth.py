from pydantic import BaseModel, EmailStr

class OTPRequest(BaseModel):
    email: EmailStr


class OTPVerifyRequest(BaseModel):
    email: EmailStr
    otp: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str