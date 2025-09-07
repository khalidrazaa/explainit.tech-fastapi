from pydantic import BaseModel, EmailStr

class OTPRequest(BaseModel):
    email: EmailStr


class OTPVerifyRequest(BaseModel):
    email: EmailStr
    otp: str


class LoginResponse(BaseModel):
    status: bool
    token_type: str
    message: str