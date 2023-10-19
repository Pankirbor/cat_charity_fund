from fastapi import FastAPI

from app.api.routers import main_router
from app.core.config import settings
from app.core.init_db import create_first_superuser
from app.api.constans import TAGS_METADATA

app = FastAPI(title=settings.app_title, openapi_tags=TAGS_METADATA)
app.include_router(main_router)


@app.on_event("startup")
async def startup():
    await create_first_superuser()
