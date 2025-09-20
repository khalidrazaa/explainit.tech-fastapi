import os
from typing import List, Dict, Any, Optional
from datetime import datetime
import asyncio

import httpx
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.models.keyword import Keyword
from app.schemas.keyword import KeywordSuggestion, KeywordResponse

SERP_API_KEY = os.getenv("SERPAPI_KEY")
BASE_URL = os.getenv("SERPAPI_BASE_URL")


class KeywordService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def _http_get(self, params: dict) -> dict:
        async with httpx.AsyncClient(timeout=20.0) as client:
            r = await client.get(BASE_URL, params=params)
            r.raise_for_status()
            return r.json() or {}

    # --- Fetch methods ---
    async def fetch_google_autocomplete(self, keyword: str) -> List[str]:
        try:
            params = {"engine": "google_autocomplete", "q": keyword, "api_key": SERP_API_KEY}
            data = await self._http_get(params)
            suggestions = data.get("suggestions") or []
            return [s.get("value") for s in suggestions if s.get("value")]
        except Exception:
            return []

    async def fetch_google_trends(self, keyword: str) -> float:
        try:
            params = {"engine": "google_trends", "q": keyword, "api_key": SERP_API_KEY}
            data = await self._http_get(params)
            arr = data.get("interest_over_time") or []
            if not arr:
                return 0.0
            return float(arr[-1].get("value", 0) or 0)
        except Exception:
            return 0.0

    async def fetch_google_search_related(self, keyword: str) -> List[str]:
        try:
            params = {"engine": "google", "q": keyword, "api_key": SERP_API_KEY}
            data = await self._http_get(params)
            related = data.get("related_searches") or []
            result = []
            for item in related:
                if isinstance(item, dict):
                    result.append(item.get("query") or item.get("value"))
                else:
                    result.append(item)
            return [r for r in result if r]
        except Exception:
            return []

    async def fetch_youtube(self, keyword: str) -> List[str]:
        try:
            params = {"engine": "youtube", "search_query": keyword, "api_key": SERP_API_KEY}
            data = await self._http_get(params)
            videos = data.get("video_results") or []
            return [v.get("title") for v in videos if v.get("title")]
        except Exception:
            return []

    async def fetch_news(self, keyword: str) -> List[str]:
        try:
            params = {"engine": "google_news", "q": keyword, "api_key": SERP_API_KEY}
            data = await self._http_get(params)
            news = data.get("news_results") or []
            return [n.get("title") for n in news if n.get("title")]
        except Exception:
            return []

    # --- DB functions ---
    async def _db_get_keyword(self, keyword: str) -> Optional[Keyword]:
        stmt = select(Keyword).where(Keyword.keyword == keyword)
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def _db_create_keyword(self, keyword: str, source: str, suggestions: List[Dict[str, str]]) -> Keyword:
        obj = Keyword(
            keyword=keyword,
            source=source,
            monthly_searches=None,
            cpc=None,
            seo_difficulty=None,
            suggestions=suggestions,
            processed=False,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        self.db.add(obj)
        await self.db.commit()
        await self.db.refresh(obj)
        return obj

    # --- Main function ---
    async def get_keyword_data(self, keyword: str) -> dict:
        # 1) Check DB
        db_keyword = await self._db_get_keyword(keyword)
        if db_keyword:
            saved = db_keyword.suggestions or []
            suggestions = [
                KeywordSuggestion(suggestion=item.get("suggestion"), source=item.get("source", ""))
                for item in saved
            ]
            return {
                "status": "ok",
                "keyword": db_keyword.keyword,
                "suggestions": suggestions,
                "monthly_searches": db_keyword.monthly_searches,
                "cpc": db_keyword.cpc,
                "seo_difficulty": db_keyword.seo_difficulty,
                "trend_score": 0.0  # DB may not have trends stored
            }

        # 2) Fetch from all sources concurrently
        auto, trend_score, related, youtube, news = await self._gather_sources(keyword)

        # Build unique list
        seen = set()
        suggestions_list: List[Dict[str, str]] = []

        def add_suggestions(items: List[str], src: str):
            for s in (items or []):
                key = (s or "").strip().lower()
                if key and key not in seen:
                    seen.add(key)
                    suggestions_list.append({"suggestion": s, "source": src})

        add_suggestions(auto, "google_autocomplete")
        add_suggestions(related, "google_related")
        add_suggestions(youtube, "youtube")
        add_suggestions(news, "news")

        # 3) Persist new keyword
        created = await self._db_create_keyword(keyword, "mixed", suggestions_list)

        # 4) Build response
        resp_suggestions = [
            KeywordSuggestion(suggestion=item["suggestion"], source=item["source"]) for item in suggestions_list
        ]

        return {
            "status": "ok",
            "keyword": keyword,
            "suggestions": resp_suggestions,
            "monthly_searches": created.monthly_searches,
            "cpc": created.cpc,
            "seo_difficulty": created.seo_difficulty,
            "trend_score": trend_score,
        }

    async def _gather_sources(self, keyword: str):
        """Run all source fetches concurrently, safely returning defaults if any fail."""
        tasks = [
            self.fetch_google_autocomplete(keyword),
            self.fetch_google_trends(keyword),
            self.fetch_google_search_related(keyword),
            self.fetch_youtube(keyword),
            self.fetch_news(keyword),
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        final_results = []
        for r in results:
            if isinstance(r, Exception):
                # Determine type based on index of task
                final_results.append([] if isinstance(r, list) else 0.0)
            else:
                final_results.append(r)
        return final_results  # auto, trend_score, related, youtube, news