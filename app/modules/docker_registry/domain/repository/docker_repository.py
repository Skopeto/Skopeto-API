from abc import ABC, abstractmethod
from app.modules.docker_registry.domain.entity.docker_container import DockerContainer

class DockerRepositoryInterface(ABC):
    @abstractmethod
    async def persist_docker_container(self, docker_container: DockerContainer) -> DockerContainer:
        raise NotImplementedError()