from abc import ABC, abstractmethod
from app.modules.server_registry.domain.entity.server import Server


class ServerRepositoryInterface(ABC):
    @abstractmethod
    def persist_server(self, server: Server) -> Server:
        raise NotImplementedError()