from fastapi import status, APIRouter, Depends, Request, HTTPException
from src.v1.schemas.url import URLIN, URLOUT, URLUpdate, URLStatsResponse
from src.v1.service.url import URLService
from src.database.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.responses import RedirectResponse
from src.v1.models.model import URLS
from sqlmodel import select, desc
from datetime import datetime
import logging


logger = logging.getLogger(__name__)
url_service = URLService()
url_router = APIRouter()

@url_router.post("/shorten", status_code=status.HTTP_201_CREATED)
async def create_short_url(url:URLIN, session: AsyncSession = Depends(get_session)):
    shorten_url = await url_service.create_short_url(url=url, session=session)
    return shorten_url

@url_router.get("/shorten", status_code=status.HTTP_200_OK, response_model= URLOUT)
async def retrieve_original_url(short_code:str, session:AsyncSession = Depends(get_session)):
    original_url = await url_service.retrieve_original_url(short_code=short_code, session= session)
    
    return original_url


@url_router.patch("/shorten", status_code=status.HTTP_200_OK)
async def update_original_url(short_code:str, original_url:URLUpdate, session:AsyncSession=Depends(get_session)):
    url_to_update = await url_service.update_original_url(short_code=short_code, update_item=original_url,session=session)
    return url_to_update


@url_router.delete("/shorten", status_code=status.HTTP_204_NO_CONTENT)
async def delete_short_code(short_code:str, session:AsyncSession=Depends(get_session)):
    await url_service.delete_short_url(short_code=short_code, session=session)
    
    return {"message":"Short URL deleted successfully"}

@url_router.get("/shorten/{short_code}/stats", response_model=URLStatsResponse)
async def get_short_url_stats(short_code: str, session: AsyncSession = Depends(get_session)):
    return await url_service.get_url_stats(short_code, session)

@url_router.get("/{short_code}")
async def redirect_to_original_url(short_code:str,request:Request, session: AsyncSession = Depends(get_session)):
    statement = select(URLS).where(URLS.short_code == short_code)
    result = await session.exec(statement)
    url = result.first()
    
    
    if not url:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Short URL not found")
    
    url.access_count +=1 
    url.updated_at = datetime.utcnow()
    
    session.add(url)
    await session.commit()
    
    ip = request.client.host
    agent = request.headers.get("user-agent")
    logger.info(f"Redirected {short_code} accessed by {ip} using {agent}")
    
    return RedirectResponse(url.original_url)