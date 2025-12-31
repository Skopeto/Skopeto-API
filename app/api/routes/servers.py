from fastapi import APIRouter, Depends
import logging
import asyncio
from pydantic import BaseModel
from app.core.Exception import ApplicationException, SecurityException
from app.modules.database_registry.application.service.database_connector import DatabaseConnector
from app.modules.database_registry.application.service.database_metrics_service import DatabaseMetricsServiceInterface
from app.modules.database_registry.application.use_case.collect_database_health import collect_databases_for_server_use_case, DatabaseWithHealth
from app.modules.database_registry.domain.repository.database_repository import DatabaseRepositoryInterface
from app.modules.database_registry.infrastructure.dependencies.dependencies import get_database_connector, get_database_metrics_service, get_database_repository
from app.modules.docker_registry.application.service.docker_metrics_service import DockerMetricService
from app.modules.docker_registry.application.use_case.collect_container_metrics import collect_container_metrics_use_case
from app.modules.docker_registry.application.use_case.get_containers import get_containers_use_case
from app.modules.docker_registry.domain.repository.docker_repository import DockerRepositoryInterface
from app.modules.docker_registry.infrastructure.dependencies.dependencies import get_docker_metrics_service, get_docker_repository
from app.modules.server_registry.application.request.register_server_location_request import RegisterServerLocationRequest
from app.modules.server_registry.application.request.update_server_request import UpdateServerRequest
from app.modules.server_registry.application.service.server_metrics_service import ServerMetricsService, ServerMetricsServiceInterface
from app.modules.server_registry.application.use_case.collect_server_metrics import collect_server_metrics_use_case
from app.modules.server_registry.application.use_case.delete_server import delete_server_use_case
from app.modules.server_registry.application.use_case.edit_server import edit_server_use_case
from app.modules.server_registry.application.use_case.get_servers import get_servers_use_case
from app.modules.server_registry.application.use_case.get_server_health import get_server_health_use_case
from app.modules.server_registry.application.use_case.register_server import register_server_use_case
from app.modules.server_registry.domain.entity.server import Server
from app.modules.server_registry.domain.entity.server_health import ServerHealth
from app.modules.server_registry.domain.repository.server_repository import ServerRepositoryInterface
from app.modules.auth.domain.entity.user import User
from app.core.security import get_current_user
from app.modules.server_registry.infrastructure.dependencies.dependencies import get_server_metrics_service, get_server_repository

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/servers", tags=["Servers"])


class ServerAndDatabaseHealthResponse(BaseModel):
    server: Server
    server_health: ServerHealth
    databases: list[DatabaseWithHealth]

@router.post("/register", status_code=201)
async def register_server(
    request: RegisterServerLocationRequest,
    server_repository: ServerRepositoryInterface = Depends(get_server_repository),
    current_user: User = Depends(get_current_user)
):
    if request.registrator_id != current_user.id:
        raise SecurityException("Cannot register server for another user")

    server = await register_server_use_case(request, server_repository)
    return {"status": "success", "data": server}

@router.post("/containers/collect/{server_id}")
async def collect_server_monitoring(
    server_id: int,
    current_user: User = Depends(get_current_user),
    server_repo: ServerRepositoryInterface = Depends(get_server_repository),
    docker_repo: DockerRepositoryInterface = Depends(get_docker_repository),
    server_metrics: ServerMetricsService = Depends(get_server_metrics_service),
    docker_metrics: DockerMetricService = Depends(get_docker_metrics_service)
):
    server = await server_repo.get_server(server_id)
    if not server:
        raise ApplicationException(f"Server {server_id} not found")
    
    server_health = await collect_server_metrics_use_case(
        server_id,
        server_repo,
        server_metrics
    )
    
    containers = await collect_container_metrics_use_case(
        server_id,
        server,
        server_health,
        docker_repo,
        docker_metrics
    )
    
    return {
        "status": "success",
        "data": {
            "server": server,
            "current_health": server_health,
            "containers": containers
        }
    }

@router.get("/all-servers")
async def get_servers(
    current_user: User = Depends(get_current_user),
    server_repository: ServerRepositoryInterface = Depends(get_server_repository),
):
    servers = await get_servers_use_case(server_repository)
    return {"status": "success", "data": servers}

@router.post("/monitoring/collect-all")
async def collect_all_monitoring(
    current_user: User = Depends(get_current_user),
    server_repository: ServerRepositoryInterface = Depends(get_server_repository),
    docker_repository: DockerRepositoryInterface = Depends(get_docker_repository),
    server_metrics: ServerMetricsService = Depends(get_server_metrics_service),
    docker_metrics: DockerMetricService = Depends(get_docker_metrics_service)
):
    servers = await server_repository.get_all_servers()
    
    if not servers:
        raise ApplicationException("No servers found")
    
    async def collect_single_server(server: Server):
        if server.id is None:
            return None
        
        try:
            server_health = await collect_server_metrics_use_case(
                server.id,
                server_repository,
                server_metrics
            )
            
            containers = await collect_container_metrics_use_case(
                server.id,
                server,
                server_health,
                docker_repository,
                docker_metrics
            )
            
            return {
                "server": server,
                "current_health": server_health,
                "containers": containers
            }
        except Exception as e:
            logger.error(f"Failed to collect server {server.id}: {e}")
            return None
    
    results = await asyncio.gather(
        *[collect_single_server(server) for server in servers],
        return_exceptions=False
    )
    
    valid_results = [result for result in results if result is not None]
    
    return {"status": "success", "data": valid_results}

@router.get("/containers/all")
async def get_all_servers_and_containers(
    current_user: User = Depends(get_current_user),
    server_repo: ServerRepositoryInterface = Depends(get_server_repository),
    docker_repo: DockerRepositoryInterface = Depends(get_docker_repository),
):
    results = []
    servers = await server_repo.get_all_servers()
    for server in servers:
        if server.id is None:
            continue
        server_health = await get_server_health_use_case(server.id, server_repo)
        containers = await get_containers_use_case(server.id, docker_repo)
    
        results.append({
            "server": server,
            "server_health": server_health,
            "containers": containers
        })

    return {"status": "success", "data": results}

@router.delete('/delete/{server_id}')
async def delete_server(
    server_id: int,
    current_user: User = Depends(get_current_user),
    server_repo: ServerRepositoryInterface = Depends(get_server_repository),
):
    await delete_server_use_case(
        server_id,
        server_repo
    )
    return {"status": "success"}

@router.patch('/edit/{server_id}')
async def edit_server(
    server_id: int,
    request: UpdateServerRequest,
    current_user: User = Depends(get_current_user),
    server_repo: ServerRepositoryInterface = Depends(get_server_repository),
):
    result = await edit_server_use_case(
        server_id,
        request,
        server_repo
    )
    return {"status": "success", "data": result}


@router.get('/databases/collect/all')
async def get_databases(
    database_metrics: DatabaseMetricsServiceInterface = Depends(get_database_metrics_service),
    connector: DatabaseConnector = Depends(get_database_connector),
    database_repo: DatabaseRepositoryInterface = Depends(get_database_repository),
    server_repo: ServerRepositoryInterface = Depends(get_server_repository),
    server_metrics: ServerMetricsServiceInterface = Depends(get_server_metrics_service),
    current_user: User = Depends(get_current_user),
):
    """
    Collects database health for all servers and their databases.
    Orchestrates server and database modules.
    """
    results = []
    servers = await server_repo.get_all_servers()

    for server in servers:
        if server.id is None:
            continue

        # Get server health (server module)
        server_health_dict = await server_metrics.get_server_metrics(server)
        server_health = ServerHealth(**server_health_dict)

        # Get databases with health (database module - pass only server_id)
        databases = await collect_databases_for_server_use_case(
            server.id,
            database_repo,
            database_metrics,
            connector,
        )

        # Combine results (orchestration)
        results.append(
            ServerAndDatabaseHealthResponse(
                server=server,
                server_health=server_health,
                databases=databases,
            )
        )

    return {"status": "success", "data": results}