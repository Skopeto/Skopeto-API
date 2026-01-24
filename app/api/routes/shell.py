from fastapi import APIRouter, Depends, WebSocket
import logging
from app.core.db_session import SessionManager
from app.modules.server_registry.infrastructure.sql_repository.server_repository import SqlServerRepository
from app.modules.server_registry.application.use_case.interactive_shell import interactive_shell_use_case
from app.modules.server_registry.infrastructure.dependencies.dependencies import get_shell_service

logger = logging.getLogger(__name__)
router = APIRouter()

@router.websocket("/ws/shell/{server_id}")
async def websocket_shell(
    websocket: WebSocket,
    server_id: int,
    shell_service = Depends(get_shell_service)
):
    async with SessionManager.session_scope() as session:
        server_repository = SqlServerRepository(session)
        server = await server_repository.get_server(server_id)
    
    if not server:
        await websocket.accept()
        await websocket.send_json({"type": "error", "data": f"Server {server_id} not found"})
        await websocket.close()
        return
    
    await interactive_shell_use_case(
        websocket=websocket,
        server=server,
        shell_service=shell_service
    )