from abc import ABC, abstractmethod
from app.modules.server_health_ckeck.domain.entity.heallth_check import ServerCheck
from app.modules.server_registry.domain.entity.server import Server
from app.modules.server_registry.domain.entity.server_check_history import ServerCheckHistory


class ServerRepositoryInterface(ABC):
    @abstractmethod
    async def get_all_servers(self) -> list[Server]:
        raise NotImplementedError()

    @abstractmethod
    async def persist_server(self, server: Server) -> Server:
        raise NotImplementedError()

    @abstractmethod
    async def get_server(self, server_id: int) -> Server | None:
        raise NotImplementedError()

    @abstractmethod
    async def persist_server_check_history(self, server_check_history: ServerCheckHistory) -> ServerCheckHistory:
        raise NotImplementedError()

    @abstractmethod
    async def delete_server(self, server_id) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def update_server(self, Server: Server) -> Server:
        raise NotImplementedError()

    @abstractmethod
    async def get_server_checks(self) -> list[ServerCheck]:
        raise NotImplementedError()