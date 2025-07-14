from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.database.main import init,close_db
from src.utils.logging_conf import configure_logging


@asynccontextmanager
async def lifespan(app:FastAPI):
    print("App starting")
    configure_logging()
    await init()
    yield
    await close_db()
    print("Shutdown completed")
    
version ="v1"
version_prefix= f"/api/{version}"

app = FastAPI(
    title="URL Shortner API",
    description="A simple RESTful API that allows users to shorten long URLs. This API provides endpoints to create, retrieve, update, and delete short URLs. It also provide statistics on the number of times a short URL has been accessed.",
    version=version,
    lifespan=lifespan
)

# Connect routes here
# app.include_router()