from abc import ABC, abstractmethod

from app.modules.server_health_ckeck.domain.entity.heallth_check import ServerCheck


class ServerCheckRepositoryInterface(ABC):
    @abstractmethod
    async def create_server_check(self, server_check: ServerCheck) -> None:
        pass

    @abstractmethod
    async def get_server_checks(self) -> list[ServerCheck]:
        pass

    @abstractmethod
    async def get_server_check(self, health_check_id: int) -> ServerCheck | None:
        pass

    @abstractmethod
    async def update_server_check(self, server_check: ServerCheck) -> ServerCheck:
        pass

    @abstractmethod
    async def delete_server_check(self, health_check_id: int) -> None:
        pass
