from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.auth import OTPRequest, OTPVerifyRequest, LoginResponse
from app.services.auth_service import send_otp_service, verify_otp_service

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/send-otp")
async def send_otp(payload: OTPRequest, db: AsyncSession = Depends(get_db)):
    return await send_otp_service(payload.email, db)

@router.post("/verify-otp", response_model=LoginResponse)
async def verify_otp(payload: OTPVerifyRequest, db: AsyncSession = Depends(get_db)):
    return await verify_otp_service(payload.email, payload.otp, db)
