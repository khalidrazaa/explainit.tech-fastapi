from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.session import get_db
from app.db.models.admin_user import AdminUser
from app.core.security import verify_password, create_access_token

async def authenticate_user(username: str, password: str, db: AsyncSession):
    result = await db.execute(select(AdminUser).where(AdminUser.username == username))
    user = result.scalars().first()

    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(data={"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}