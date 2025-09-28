from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.keyword import KeywordRequest, KeywordResponse
from app.services.keyword_service import KeywordService
from app.db.session import get_db
from app.services.trend_scrape import TrendsScraper

router = APIRouter()


@router.post("/keywords", response_model=KeywordResponse)
async def get_keywords(req: KeywordRequest, db: AsyncSession = Depends(get_db)):
    if not req.keyword or not req.keyword.strip():
        raise HTTPException(status_code=400, detail="keyword is required")
    
    service = KeywordService(db)
    return await service.get_keyword_data(req.keyword.strip())

@router.post("/scrape")
async def scrape_trends(geo:str, hours:str, sts:str):
    scraper = TrendsScraper()
    print("scrape", geo, hours, sts)
    csv_bytes = await scraper.fetch_trending_csv_bytes(geo, hours, sts)
    inserted_count, operations = scraper.save_csv_bytes_to_mongo(csv_bytes)
    return {
        "status": True,
        "geo": geo,
        "hours": hours,
        "operations":operations,
        "processed_rows":inserted_count, 
    }