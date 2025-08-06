from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.db.session import get_db
from app.db.models.admin_user import AdminUser  # your actual Admin model
from app.schemas.admin_user import AdminUserCreate  # your actual schema
from app.db.services.admin_service import create_admin

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.post("/create", status_code=201)
async def create_admin(payload: AdminUserCreate, db: AsyncSession = Depends(get_db)):
    admin = await create_admin(payload, db)
    return JSONResponse(content={"message": "Admin created successfully", "admin_id": admin.id},
                        status_code=201)