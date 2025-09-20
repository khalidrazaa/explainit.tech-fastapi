from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.keyword import KeywordRequest, KeywordResponse
from app.services.keyword_service import KeywordService
from app.db.session import get_db

router = APIRouter()


@router.post("/keywords", response_model=KeywordResponse)
async def get_keywords(req: KeywordRequest, db: AsyncSession = Depends(get_db)):
    if not req.keyword or not req.keyword.strip():
        raise HTTPException(status_code=400, detail="keyword is required")
    
    service = KeywordService(db)
    return await service.get_keyword_data(req.keyword.strip())
