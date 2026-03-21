from abc import ABC, abstractmethod
from app.modules.docker_registry.domain.entity.docker_container import DockerContainer

class DockerRepositoryInterface(ABC):
    @abstractmethod
    async def persist_docker_container(self, docker_container: DockerContainer) -> DockerContainer:
        raise NotImplementedError()

    @abstractmethod
    async def update_docker_container(self, docker_container: DockerContainer) -> DockerContainer:
        raise NotImplementedError()

    @abstractmethod
    async def get_docker_container(self, name: str, server_id: int) -> DockerContainer | None:
        raise NotImplementedError()

    @abstractmethod
    async def get_docker_containers(self, server_id: int) -> list[DockerContainer]:
        raise NotImplementedError()

    @abstractmethod
    async def upsert_docker_containers(self, containers: list[DockerContainer]) -> list[DockerContainer]:
        raise NotImplementedError()