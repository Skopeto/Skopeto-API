from app.modules.docker_registry.domain.entity.docker_container import DockerContainer
from app.modules.docker_registry.domain.repository.docker_repository import DockerRepositoryInterface

def register_docker_container_use_case(
    docker_container_data: DockerContainer, 
    docker_repository: DockerRepositoryInterface
) -> DockerContainer:
    return docker_repository.persist_docker_container(docker_container_data)