from app.core.Exception import ApplicationException
from app.modules.server_registry.application.request.update_server_request import (
    UpdateServerRequest,
)
from app.modules.server_registry.domain.entity.server import Server
from app.modules.server_registry.domain.entity.server_status import ServerStatus
from app.modules.server_registry.domain.repository.server_repository import (
    ServerRepositoryInterface,
)
from app.core.encrypt import encrypt_password


async def edit_server_use_case(
    server_id: int,
    request: UpdateServerRequest,
    server_repository: ServerRepositoryInterface,
) -> Server:
    server = await server_repository.get_server(server_id)

    if not server:
        raise ApplicationException(f"Server {server_id} not found")

    updates = {}

    if request.name is not None:
        updates["user_name"] = request.name
    if request.password is not None:
        updates["ssh_password_encrypted"] = encrypt_password(request.password)
    if request.ip_address is not None:
        updates["ip_address"] = request.ip_address
    if request.port is not None:
        updates["port"] = request.port
    if request.status is not None:
        updates["status"] = ServerStatus(request.status)

    server = server.model_copy(update=updates)
    return await server_repository.update_server(server)
