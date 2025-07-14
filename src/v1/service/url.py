from fastapi import HTTPException,status
from sqlmodel import select, desc
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy import func, extract
from src.v1.models.model import URLS
from src.v1.schemas.url import URLIN, URLUpdate, URLStatsResponse
import logging
import uuid
from typing import Optional
from datetime import datetime
import string, random


logger = logging.getLogger(__name__)

class URLService:
    async def create_short_url(self, url:URLIN, session:AsyncSession) -> dict:
        # Generate a unique short code
        short_code = await self.generate_unique_code(session=session)
        
        # Store in DB
        now = datetime.utcnow()
        new_url = URLS(original_url=url.url,short_code=short_code, created_at=now, updated_at=now, access_count=0)
        
        session.add(new_url)
        await session.commit()
        await session.refresh(new_url)
        return new_url
    
    async def generate_unique_code(self, session:AsyncSession, length: int = 6 ) -> str:
        chars = string.ascii_letters + string.digits
        while True:
            code =''.join(random.choices(chars, k=length))
            
            statement = select(URLS).where(URLS.short_code == code)
            result = await session.exec(statement)
            existing_url = result.first()
            
            if not existing_url:
                return code  
            
    
    async def retrieve_original_url(self,short_code:str,session:AsyncSession) -> dict:
        statement = select(URLS).where(URLS.short_code == short_code)
        result = await session.exec(statement)
        original_result = result.first()
        return original_result
            
            
    async def update_original_url(self, short_code:str, update_item:URLUpdate, session:AsyncSession) -> dict:
        statement = select(URLS).where(URLS.short_code == short_code)
        result = await session.exec(statement)
        url = result.first()
        
        if not url:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Short code {short_code} not found")
        
        url_to_update = update_item.model_dump(exclude_unset=True)
            
        for k,v in url_to_update.items():
            setattr(url,k,v)
        
        session.add(url)
        await session.commit()
        await session.refresh(url)
        return url
    
    
    async def delete_short_url(self,short_code:str, session:AsyncSession):
        short_code = await self.retrieve_original_url(short_code=short_code, session=session)
        
        if not short_code: 
            raise  HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Short code {short_code} doesn't exist")
        
        await session.delete(short_code)
        await session.commit()

    async def get_url_stats(self,short_code:str, session:AsyncSession) -> URLStatsResponse:
        url = await self.retrieve_original_url(short_code=short_code, session=session)
        
        if not url:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Short code {short_code} not found")
        
        return  URLStatsResponse(
            short_code= url.short_code,
            original_code=url.original_url,
            access_count=url.access_count,
            created_at=url.created_at,
            updated_at=url.updated_at
        )