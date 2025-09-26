from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class TrendItem(BaseModel):
    trend: str
    search_volume: Optional[str]
    started: Optional[datetime]
    ended: Optional[datetime]
    trend_breakdown: Optional[List[str]] = []
    explore_link: Optional[str]