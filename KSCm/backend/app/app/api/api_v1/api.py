from fastapi import APIRouter

from app.api.api_v1.endpoints import items, login, users, utils, stores, tickets, claims

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
api_router.include_router(items.router, prefix="/items", tags=["items"])
api_router.include_router(stores.router, prefix="/stores", tags=["stores"])
api_router.include_router(tickets.router, prefix="/tickets", tags=["tickets"])
api_router.include_router(claims.router, prefix="/claims", tags=["claims"])
