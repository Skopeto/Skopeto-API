from app.modules.database_registry.domain.repository.database_repository import DatabaseRepositoryInterface

async def delete_database_use_case(
    database_id: int,
    database_repo: DatabaseRepositoryInterface
) -> None:
    existing_db = await database_repo.get_database_by_id(database_id)
    if not existing_db:
        raise ValueError("Database not found")
    
    await database_repo.delete_database(database_id)