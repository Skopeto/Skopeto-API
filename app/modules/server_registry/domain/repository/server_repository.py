from abc import ABC, abstractmethod
from app.modules.server_registry.domain.entity.server import Server
from app.modules.server_registry.domain.entity.server_health import ServerHealth
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
    async def persist_server_health(self, server_health: ServerHealth) -> ServerHealth:
        raise NotImplementedError()
    
    @abstractmethod
    async def get_server_health(self, server_id: int) -> ServerHealth | None:
        raise NotImplementedError()
    
    @abstractmethod
    async def update_server_health(self,server_id: int, server_health: ServerHealth) -> ServerHealth | None:
        raise NotImplementedError()
    
    @abstractmethod
    async def persist_server_health_history(self, server_health: ServerHistory) -> ServerHistory:
        raise NotImplementedError()