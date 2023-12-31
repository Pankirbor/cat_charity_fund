from fastapi import FastAPI

from app.api.routers import main_router
from app.core.config import settings
from app.core.init_db import create_first_superuser
from app.constants import TAGS_METADATA

app = FastAPI(title=settings.app_title, openapi_tags=TAGS_METADATA)
app.include_router(main_router)


@app.on_event("startup")
async def startup():
    """Функция автоматического создания суперюзера при первом запуске приложения."""
    await create_first_superuser()
