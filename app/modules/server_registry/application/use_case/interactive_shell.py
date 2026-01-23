import logging
from fastapi import WebSocket
from app.core.Exception import ApplicationException
from app.modules.server_registry.application.service.shell_service import ServerShellServiceInterface
from app.modules.server_registry.domain.repository.server_repository import ServerRepositoryInterface

logger = logging.getLogger(__name__)

async def interactive_shell_use_case(
    websocket: WebSocket,
    server_id: int,
    server_repository: ServerRepositoryInterface,
    shell_service: ServerShellServiceInterface
):
    await websocket.accept()
    
    try:
        server = await server_repository.get_server(server_id)
        if not server:
            await websocket.send_json({"type": "error", "data": f"Server {server_id} not found"})
            await websocket.close()
            return
        
        await shell_service.start_interactive_shell(websocket, server)
        
    except ApplicationException as e:
        logger.error(f"Application error for server {server_id}: {e}")
        await websocket.send_json({"type": "error", "data": str(e)})
    except Exception as e:
        logger.error(f"Failed to start shell for server {server_id}: {e}", exc_info=True)
        await websocket.send_json({"type": "error", "data": "Failed to start shell session"})
    finally:
        try:
            await websocket.close()
        except:
            pass