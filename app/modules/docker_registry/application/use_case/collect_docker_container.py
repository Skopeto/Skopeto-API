from app.modules.docker_registry.application.service.docker_metrics_service import DockerMetricService
from app.modules.docker_registry.domain.entity.docker_container import DockerContainer
from app.modules.docker_registry.domain.repository.docker_repository import DockerRepositoryInterface
from app.modules.server_registry.domain.entity.server import Server
from app.modules.server_registry.domain.repository.server_repository import ServerRepositoryInterface

def server_exists_and_is_valid(
    server_id: int,
    server_repo: ServerRepositoryInterface
) -> Server:
    server = server_repo.get_server(server_id)
    
    if not server:
        raise Exception(server_id)
    
    return server

async def collect_docker_container_data_use_case(
    server_id: int, 
    docker_service: DockerMetricService,
    server_repository: ServerRepositoryInterface,
    docker_repository: DockerRepositoryInterface
) -> list[DockerContainer]:
    server = server_exists_and_is_valid(server_id, server_repository)
    docker_container_data = docker_service.get_docker_metrics(server)
    
    persisted_containers = []
    for container_data in docker_container_data:
        docker_container = DockerContainer(**container_data)
        persisted_container = await docker_repository.persist_docker_container(docker_container)
        persisted_containers.append(persisted_container)
    
    return persisted_containers