from fastapi import APIRouter

from app.views.endpoints import reporting, websockets


view_router = APIRouter()
view_router.include_router(reporting.router, tags=["reporting"])
view_router.include_router(websockets.router, tags=["websockets"])
