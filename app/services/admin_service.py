from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException

from app.db.models.admin_user import AdminUser
from app.schemas.admin_user import AdminUserCreate
from app.services.auth_service import send_otp_service

import datetime
from googletrends import get_trending_topics   # <- placeholder for your logic
from llm_client import generate_article        # <- placeholder for your LLM API client

async def create_admin_service(payload: AdminUserCreate, db: AsyncSession):
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
    
    otp = await send_otp_service(admin.email, db)
    if otp["status"] == False:
        raise HTTPException(status_code=400, detail=otp["message"])

    return {admin : admin, "status": True, "message": "Admin created successfully"}


async def get_google_trends_topics(category: str):
    """
    Fetch trending topics from Google Trends API / scraper.
    """
    # Example - Replace with real fetch logic
    trends = await get_trending_topics(category)
    return {"status": True, "category": category, "topics": trends}


async def generate_article_from_topic(topic: str):
    """
    Generate an article draft using LLM based on a selected trend.
    """
    # Call LLM API to generate structured article
    article = await generate_article(topic)

    # Add metadata
    article["id"] = f"art_{datetime.datetime.utcnow().timestamp()}"
    article["status"] = "draft"
    article["createdAt"] = datetime.datetime.utcnow().isoformat()

    # TODO: Save to Mongo/Postgres (depending on your DB)
    # db.articles.insert_one(article)

    return {"status": True, "article": article}