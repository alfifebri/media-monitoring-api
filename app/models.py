from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from app.database import Base

class Mention(Base):
    __tablename__ = "mentions"

    id = Column(Integer, primary_key=True, index=True)
    external_id = Column(String(255), nullable=True)
    source = Column(String(100), nullable=False, index=True)
    title = Column(Text, nullable=True)
    content = Column(Text, nullable=False)
    url = Column(Text, unique=True, nullable=False)
    author = Column(String(255), nullable=True)
    published_at = Column(DateTime(timezone=True), nullable=True, index=True)
    engagement = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())