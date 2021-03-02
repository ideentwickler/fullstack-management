from typing import List
from fastapi import APIRouter, Depends

from fastapi import  WebSocket, WebSocketDisconnect

from app.api.deps import get_current_active_user
from app.api.api_v1.endpoints import (
    login, users, utils, stores, tickets, claims, controlling, media
)

# GLOBAL USER DEPENDENCY
USER_DEPENDS = [] #[Depends(get_current_active_user)]

# INIT ROUTER
api_router = APIRouter()

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()


@api_router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast(f"Client #{client_id} says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat")


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
