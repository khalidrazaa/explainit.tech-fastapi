from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException

from app.db.models.admin_user import AdminUser
from app.schemas.admin_user import AdminUserCreate

async def create_admin(payload: AdminUserCreate, db: AsyncSession):
    result = await db.execute(select(AdminUser).where(AdminUser.email == payload.email))
    existing_admin = result.scalar_one_or_none()

    if existing_admin:
        raise HTTPException(status_code=400, detail="Admin already exists")

    admin = AdminUser(
        email=payload.email,
        phone=payload.phone,
        full_name=payload.full_name,
        gender=payload.gender,
        dob=payload.dob,
    )

    db.add(admin)
    await db.commit()
    await db.refresh(admin)

    return admin