from pydantic import BaseModel
from datetime import datetime
import uuid
from typing import Optional

class URLIN(BaseModel):
    url:str
    
    
class URLOUT(BaseModel):
    uid : uuid.UUID 
    short_code: str
    original_url: str
    access_count: int
    created_at: datetime 
    updated_at: datetime 
    
    
class URLUpdate(BaseModel):
    original_url:Optional[str]
    
class URLStatsResponse(BaseModel):
    short_code: str
    original_code:str
    access_count: int
    created_at: datetime
    updated_at: datetime
    
    