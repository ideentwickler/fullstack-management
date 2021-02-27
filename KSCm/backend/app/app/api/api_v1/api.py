from fastapi import APIRouter, Depends

from app.api.deps import get_current_active_user
from app.api.api_v1.endpoints import (
    login, users, utils, stores, tickets, claims, controlling, media
)

# GLOBAL USER DEPENDENCY
USER_DEPENDS = [] #[Depends(get_current_active_user)]

# INIT ROUTER
api_router = APIRouter()

# ROUTER WITHOUT USER DEPENDENCY
api_router.include_router(login.router, tags=["login"])

# ROUTERS WITH USER DEPENDENCY
api_router.include_router(users.router, prefix="/users", tags=["users"],
                          dependencies=USER_DEPENDS)
api_router.include_router(utils.router, prefix="/utils", tags=["utils"],
                          dependencies=USER_DEPENDS)
api_router.include_router(stores.router, prefix="/stores", tags=["stores"],
                          dependencies=USER_DEPENDS)
api_router.include_router(tickets.router, prefix="/tickets", tags=["tickets"],
                          dependencies=USER_DEPENDS)
api_router.include_router(claims.router, prefix="/claims", tags=["claims"],
                          dependencies=USER_DEPENDS)
api_router.include_router(controlling.router, prefix="/controlling",
                          tags=["controlling"],
                          dependencies=USER_DEPENDS)
api_router.include_router(media.router, prefix="/media", tags=["media"],
                          dependencies=USER_DEPENDS)
