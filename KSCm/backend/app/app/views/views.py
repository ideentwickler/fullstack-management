from fastapi import APIRouter

from app.views.endpoints import reporting


view_router = APIRouter()
view_router.include_router(reporting.router, tags=["reporting"])
