from app.modules.server_registry.domain.repository.server_repository import ServerRepositoryInterface

async def delete_server_use_case(server_id: int, server_repository: ServerRepositoryInterface) -> None:
    return await server_repository.delete_server(server_id)