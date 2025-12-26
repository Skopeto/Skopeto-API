from pydantic import BaseModel
from app.core.Exception import ApplicationException
from app.modules.server_registry.domain.entity.server import Server
from app.modules.server_registry.domain.entity.server_health import ServerHealth
from app.modules.docker_registry.domain.entity.docker_container import DockerContainer
from app.modules.server_registry.domain.repository.server_repository import ServerRepositoryInterface
from app.modules.docker_registry.domain.repository.docker_repository import DockerRepositoryInterface
import logging

logger = logging.getLogger(__name__)

class ServersAndContainersResult(BaseModel):
    server: Server
    current_health: ServerHealth | None
    containers: list[DockerContainer]

async def get_all_servers_containers_use_case(
    server_repository: ServerRepositoryInterface,
    docker_repository: DockerRepositoryInterface,
) -> list[ServersAndContainersResult]:
    
    servers = await server_repository.get_all_servers()
    if not servers:
        raise ApplicationException("No servers found")
    
    results = []
    for server in servers:
        if server.id is None:
            logger.warning(f"Skipping server with no ID: {server}")
            continue
        
        containers = await docker_repository.get_docker_containers(server.id)
        server_health = await server_repository.get_server_health(server.id)
        
        results.append(ServersAndContainersResult(
            server=server,
            current_health=server_health,
            containers=containers
        ))
    
    return results