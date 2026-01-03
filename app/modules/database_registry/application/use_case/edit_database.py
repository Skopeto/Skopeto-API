from app.modules.database_registry.application.request.update_database_request import (
    UpdateDatabaseRequest,
)
from app.modules.database_registry.domain.entity.database import Database
from app.modules.database_registry.domain.repository.database_repository import (
    DatabaseRepositoryInterface,
)
from app.core.encrypt import encrypt_password


async def edit_database_use_case(
    id: int,
    request: UpdateDatabaseRequest,
    database_repository: DatabaseRepositoryInterface,
) -> Database:
    database = await database_repository.get_database_by_id(id)

    if not database:
        raise Exception(f"Database with ID {id} not found")
    if request.name is not None:
        database.name = request.name
    if request.db_type is not None:
        database.db_type = request.db_type
    if request.host is not None:
        database.host = request.host
    if request.port is not None:
        database.port = request.port
    if request.database_name is not None:
        database.database_name = request.database_name
    if request.service_name is not None:
        database.service_name = request.service_name
    if request.username is not None:
        database.username = request.username
    if request.password is not None:
        database.encrypted_password = encrypt_password(request.password)

    return await database_repository.update_database(database)
