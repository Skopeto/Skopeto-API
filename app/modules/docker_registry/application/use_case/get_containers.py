from pydantic import BaseModel
from app.core.Exception import ApplicationException
from app.modules.server_registry.domain.entity.server import Server
from app.modules.server_registry.domain.entity.server_health import ServerHealth
from app.modules.docker_registry.domain.entity.docker_container import DockerContainer
from app.modules.docker_registry.domain.repository.docker_repository import DockerRepositoryInterface
import logging

logger = logging.getLogger(__name__)

async def get_containers_use_case(
    server_id : int,
    docker_repository: DockerRepositoryInterface,
) -> list[DockerContainer]:

    containers = await docker_repository.get_docker_containers(server_id)
        
    return containers