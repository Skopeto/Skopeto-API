import logging
from fastapi import WebSocket
from app.core.Exception import ApplicationException
from app.modules.server_registry.application.service.shell_service import ServerShellServiceInterface
from app.modules.server_registry.domain.entity.server import Server

logger = logging.getLogger(__name__)

async def interactive_shell_use_case(
    websocket: WebSocket,
    server: Server,
    shell_service: ServerShellServiceInterface
):
    await websocket.accept()
    
    try:
        await shell_service.start_interactive_shell(websocket, server)
    except ApplicationException as e:
        logger.error(f"Application error for server {server.id}: {e}")
        await websocket.send_json({"type": "error", "data": str(e)})
    except Exception as e:
        logger.error(f"Failed to start shell for server {server.id}: {e}", exc_info=True)
        await websocket.send_json({"type": "error", "data": "Failed to start shell session"})
    finally:
        try:
            await websocket.close()
        except:
            pass