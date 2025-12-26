from app.modules.server_registry.domain.entity.server import Server
from app.modules.server_registry.domain.repository.server_repository import ServerRepositoryInterface

async def get_servers_use_case(server_repository: ServerRepositoryInterface) -> list[Server]:
    servers = await server_repository.get_all_servers()
    return servers