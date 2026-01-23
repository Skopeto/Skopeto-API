from fastapi import APIRouter, Depends, WebSocket

from app.modules.server_registry.application.use_case.interactive_shell import interactive_shell_use_case
from app.modules.server_registry.infrastructure.dependencies.dependencies import get_server_repository, get_shell_service

router = APIRouter()

@router.websocket("/ws/shell/{server_id}")
async def websocket_shell(
    websocket: WebSocket,
    server_id: int,
    server_repository = Depends(get_server_repository),
    shell_service = Depends(get_shell_service)
):
    await interactive_shell_use_case(
        websocket=websocket,
        server_id=server_id,
        server_repository=server_repository,
        shell_service=shell_service
    )