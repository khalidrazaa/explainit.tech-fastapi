from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, JSON
from sqlalchemy.sql import func
from app.db.session import Base

class Keyword(Base):
    __tablename__ = "keywords"

    id = Column(Integer, primary_key=True, index=True)
    keyword = Column(String, unique=True, index=True, nullable=False)
    source = Column(String, nullable=True)  # e.g., google, youtube, reddit
    monthly_searches = Column(Integer, nullable=True)
    cpc = Column(Float, nullable=True)  # Cost per click
    seo_difficulty = Column(Float, nullable=True)

    # store fetched suggestions as JSON: [{"suggestion":"ai tools", "source":"google_autocomplete"}, ...]
    suggestions = Column(JSON, default=[])

    processed = Column(Boolean, default=False)  # whether an article has been generated for this keyword
    article_id = Column(Integer, nullable=True)  # link to Article table if processed

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
