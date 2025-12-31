from app.modules.database_registry.domain.entity.database import Database
from app.modules.database_registry.domain.repository.database_repository import DatabaseRepositoryInterface

async def get_databases_use_case(server_id: int, database_repository: DatabaseRepositoryInterface) -> list[Database]:
    return await database_repository.get_databases_by_server_id(server_id)