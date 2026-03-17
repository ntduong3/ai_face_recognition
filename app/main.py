import logging

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.controllers.recognition_controller import router as recognition_router
from app.controllers.system_controller import router as system_router
from app.controllers.users_controller import router as users_router
from app.controllers.web_controller import router as web_router
from app.core.config import settings
from app.core.logging import setup_logging

setup_logging()
logger = logging.getLogger("app")

app = FastAPI(title=settings.app_name)
app.mount("/assets", StaticFiles(directory="app/web/assets"), name="assets")
app.mount("/config", StaticFiles(directory="app/web/config"), name="config")
app.mount("/uploads", StaticFiles(directory=settings.uploads_dir), name="uploads")

app.include_router(system_router)
app.include_router(web_router)
app.include_router(users_router)
app.include_router(recognition_router)


@app.middleware("http")
async def log_requests(request, call_next):
    logger.info("%s %s", request.method, request.url.path)
    response = await call_next(request)
    logger.info("%s %s -> %s", request.method, request.url.path, response.status_code)
    return response
