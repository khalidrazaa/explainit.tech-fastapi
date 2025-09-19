from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.db.session import get_db
from app.db.models.admin_user import AdminUser  # your actual Admin model
from app.schemas.admin_user import AdminUserCreate  # your actual schema
from app.services.admin_service import create_admin_service

router = APIRouter()

@router.post("/create", status_code=201)
async def create_admin(payload: AdminUserCreate, db: AsyncSession = Depends(get_db)):
    admin = await create_admin_service(payload, db)
    print("admin", admin)
    return {"message": "Admin created successfully", "admin_id": admin.id}


@admin_router.get("/trends")
async def fetch_google_trends(
    category: str = Query("all", description="Google trends category")
):
    """Fetch trending topics from Google Trends"""
    return await get_google_trends_topics(category)


@admin_router.post("/trends/generate")
async def generate_articles_from_trends(topic: str):
    """Generate an article draft from a selected trend"""
    return await generate_article_from_topic(topic)