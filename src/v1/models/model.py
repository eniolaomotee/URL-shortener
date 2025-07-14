import uuid
from datetime import datetime
from typing import Optional
from sqlmodel import Column, Field, Relationship,SQLModel
import sqlalchemy.dialects.postgresql as pg
import logging

logger = logging.getLogger(__name__)


class URLS(SQLModel, table=True):
    __tablename__ = "urls"
    "Reps Users URLs"
    
    uid : uuid.UUID = Field(sa_column=Column(pg.UUID, primary_key=True, unique=True, nullable=False, default= uuid.uuid4))
    short_code: str
    original_url: str
    access_count: int
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP,default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    
    
    def __repr__(self) -> str:
        logger.info("Repr of  URL")
        return f"Long URL(long_url={self.original_url}, short_url={self.short_code})"
