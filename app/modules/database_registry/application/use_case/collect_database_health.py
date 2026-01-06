from app.modules.database_registry.application.service.database_connector import (
    DatabaseConnector,
)
from app.modules.database_registry.application.service.database_metrics_service import (
    DatabaseMetricsServiceInterface,
)
from app.modules.database_registry.domain.entity.database import Database
from app.modules.database_registry.domain.entity.database_health import DatabaseHealth
from app.modules.database_registry.domain.repository.database_repository import (
    DatabaseRepositoryInterface,
)
from pydantic import BaseModel
import asyncio


class DatabaseWithHealth(BaseModel):
    database: Database
    database_health: DatabaseHealth


async def collect_databases_for_server_use_case(
    server_id: int,
    database_repo: DatabaseRepositoryInterface,
    database_metrics: DatabaseMetricsServiceInterface,
    connector: DatabaseConnector,
) -> list[DatabaseWithHealth]:
    
    databases = await database_repo.get_databases_by_server_id(server_id)

    database_health_tasks = []
    for database in databases:
        if database.id:
            database_health_tasks.append(
                database_metrics.collect_health(database, connector)
            )

    health_results = await asyncio.gather(*database_health_tasks)

    databases_with_health = []
    valid_databases = [database for database in databases if database.id]

    for database, health in zip(valid_databases, health_results):
        if not database.id:
            continue
        existing = await database_repo.get_database_health(database.id)
        if existing:
            await database_repo.update_database_health(health)
        else:
            await database_repo.persist_database_health(health)

        databases_with_health.append(
            DatabaseWithHealth(database=database, database_health=health)
        )

    return databases_with_health