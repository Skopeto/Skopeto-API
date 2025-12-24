from app.modules.docker_registry.application.service.docker_metrics_service import DockerMetricService
from app.modules.docker_registry.application.use_case.register_docker_container import register_docker_container_use_case
from app.modules.docker_registry.domain.entity.docker_container import DockerContainer
from app.modules.docker_registry.domain.repository.docker_repository import DockerRepositoryInterface
from app.modules.server_registry.domain.entity.server import Server

def collect_docker_container_data_use_case(
    server: Server, 
    docker_service: DockerMetricService, 
    docker_repository: DockerRepositoryInterface
) -> list[DockerContainer]:
    docker_container_data = docker_service.get_docker_metrics(server)
    persisted_containers = []
    for container_data in docker_container_data:
        docker_container = register_docker_container_use_case.persist_docker_container(container_data)
        persisted_containers.append(docker_container)
    return persisted_containers