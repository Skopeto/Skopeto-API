from abc import ABC, abstractmethod
from app.modules.server_registry.domain.entity.server import Server
from app.modules.server_registry.domain.entity.server_health import ServerHealth

class ServerRepositoryInterface(ABC):
    @abstractmethod
    def persist_server(self, server: Server) -> Server:
        raise NotImplementedError()
    
    @abstractmethod
    def get_server(self, server_id: int) -> Server | None:
        raise NotImplementedError()
    
    @abstractmethod
    def persist_server_health(self, server_health: ServerHealth) -> ServerHealth:
        raise NotImplementedError()
    