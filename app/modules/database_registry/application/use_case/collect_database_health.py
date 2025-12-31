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
from app.modules.server_registry.application.service.server_metrics_service import (
    ServerMetricsServiceInterface,
)
from app.modules.server_registry.domain.entity.server import Server
from app.modules.server_registry.domain.entity.server_health import ServerHealth
from app.modules.server_registry.domain.repository.server_repository import (
    ServerRepositoryInterface,
)
from pydantic import BaseModel
import asyncio


class DatabaseWithHealth(BaseModel):
    database: Database
    database_health: DatabaseHealth


class ServerAndDatabaseHealthResponse(BaseModel):
    server: Server
    server_health: ServerHealth
    databases: list[DatabaseWithHealth]


async def collect_all_database_health_usecase(
    database_metrics: DatabaseMetricsServiceInterface,
    connector: DatabaseConnector,
    database_repo: DatabaseRepositoryInterface,
    server_repo: ServerRepositoryInterface,
    server_metrics: ServerMetricsServiceInterface,
) -> list[ServerAndDatabaseHealthResponse]:
    results = []
    servers = await server_repo.get_all_servers()
    
    for server in servers:
        if not server.id:
            continue
        
        server_health_dict = await server_metrics.get_server_metrics(server)
        server_health = ServerHealth(**server_health_dict)
        
        databases = await database_repo.get_databases_by_server_id(server.id)
        
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
        
        results.append(
            ServerAndDatabaseHealthResponse(
                server=server,
                server_health=server_health,
                databases=databases_with_health,
            )
        )
    
    return results