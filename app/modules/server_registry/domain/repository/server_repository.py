from abc import ABC, abstractmethod
from app.modules.server_health_ckeck.domain.entity.heallth_check import ServerCheck
from app.modules.server_registry.domain.entity.server import Server
from app.modules.server_registry.domain.entity.server_check_results import ServerCheckResults
from app.modules.server_registry.domain.entity.server_history import ServerHistory

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
    async def persist_server_check_results(self, server_check_results: ServerCheckResults) -> ServerCheckResults:
        raise NotImplementedError()
    
    @abstractmethod
    async def get_server_check_results(self, server_id: int) -> ServerCheckResults | None:
        raise NotImplementedError()
    
    @abstractmethod
    async def update_server_check_results(self,server_id: int, server_check_results: ServerCheckResults) -> ServerCheckResults | None:
        raise NotImplementedError()
    
    @abstractmethod
    async def persist_server_health_history(self, server_health: ServerHistory) -> ServerHistory:
        raise NotImplementedError()
    
    @abstractmethod
    async def delete_server(self, server_id) -> None:
        raise NotImplementedError()
    
    @abstractmethod
    async def update_server(self, Server: Server) -> Server:
        raise NotImplementedError()
    
    @abstractmethod
    async def get_server_checks(self, server_id: int) -> list[ServerCheck]:
        raise NotImplementedError()