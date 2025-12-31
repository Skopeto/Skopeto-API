from datetime import datetime, timezone
from app.modules.database_registry.application.request.register_database_request import RegisterDatabaseRequest
from app.modules.database_registry.domain.entity.database import Database
from app.modules.database_registry.domain.repository.database_repository import DatabaseRepositoryInterface
from app.core.encrypt import encrypt_password


async def register_database_use_case(
    request: RegisterDatabaseRequest,
    database_repo: DatabaseRepositoryInterface
) -> Database:
    database_data = request.model_dump()
    database_data['encrypted_password'] = encrypt_password(database_data.pop('password'))
    database_data['created_at'] = datetime.now(timezone.utc)

    database = Database(**database_data)
    return await database_repo.persist_database(database)