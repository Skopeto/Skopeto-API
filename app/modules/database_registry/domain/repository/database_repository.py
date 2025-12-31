

from abc import ABC, abstractmethod

from app.modules.database_registry.domain.entity.database import Database
from app.modules.database_registry.domain.entity.database_health import DatabaseHealth


class DatabaseRepositoryInterface(ABC):
    @abstractmethod
    async def persist_database(self, database: Database) -> Database:
        raise NotImplementedError()
    
    @abstractmethod
    async def get_database_by_name(self, name: str) -> Database:
        raise NotImplementedError()
    
    @abstractmethod
    async def get_databases_by_server_id(self, server_id: int) ->list[Database]:
        raise NotImplementedError()
    
    @abstractmethod
    async def persist_database_health(self, database_health: DatabaseHealth)-> DatabaseHealth:
        raise NotImplementedError()
    
    @abstractmethod
    async def get_database_health(self, database_id: int) -> DatabaseHealth:
        raise NotImplementedError()
    
    @abstractmethod
    async def update_database_health(self, database_health: DatabaseHealth) ->DatabaseHealth:
        raise NotImplementedError()

    # @abstractmethod
    # async def get_database_by_server_and_name(self, server_id: int, db_name: str)-> Database:
    #     raise NotImplementedError()

    
