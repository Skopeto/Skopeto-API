import datetime
from typing import Any
import logging
from app.core.Exception import RepositoryException
from app.core.base_repository import SqlBaseRepository
from app.core.sql_query import SqlQuery
from app.modules.server_registry.domain.entity.server import Server
from app.modules.server_registry.domain.entity.server_health import ServerHealth
from app.modules.server_registry.domain.entity.server_history import ServerHistory
from app.modules.server_registry.domain.repository.server_repository import ServerRepositoryInterface
from app.modules.server_registry.infrastructure.sql_query.server_query import (
    create_health_history_query,
    create_server_query,
    create_server_health_query,
    get_all_servers_query,
    get_server_health_query,
    get_server_query,
    update_server_health_query
)

logger = logging.getLogger(__name__)

def server_from_db(row: dict[str, Any] | None) -> Server | None:
    if not row:
        return None
    
    server_attrs = {
        'id': row['id'],
        'user_name': row['user_name'],
        'ssh_password_encrypted': row['ssh_password_encrypted'],
        'ip_address': row['ip_address'],
        'port': row['port'],
        'status': row['status'],
    }
    return Server.model_construct(**server_attrs)

def server_health_from_db(row: dict[str, Any] | None) -> ServerHealth |None:
    if not row:
        return None
    
    server_health_attrs = {
        'id' : row['id'],
        'server_id' : row['server_id'],
        'status' : row['status'],
        'cpu_usage' : row['cpu_usage'],
        'memory_usage' : row['memory_usage'],
        'disk_usage' : row['disk_usage'],
        'uptime' : row['uptime'],
        'checked_at' : row['checked_at'],
    }
    return ServerHealth.model_construct(**server_health_attrs)

class SqlServerRepository(ServerRepositoryInterface, SqlBaseRepository):
    async def get_server(self, server_id: int) -> Server | None:
        try:
            query, params = get_server_query(server_id)
            sql_query = SqlQuery(self.session, query, params)
            return await sql_query.fetch_one(transformer=server_from_db)
        except Exception as e:
            logger.error(f"Database error while fetching server {server_id}: {str(e)}", exc_info=True)
            raise RepositoryException("Failed to retrieve server")
    
    async def persist_server(self, server: Server) -> Server:
        try:
            query, params = create_server_query(server)
            sql_query = SqlQuery(self.session, query, params)
            await sql_query.persist()
            return server
        except Exception as e:
            logger.error(f"Database error while saving server: {str(e)}", exc_info=True)
            raise RepositoryException("Failed to save server")
    
    async def persist_server_health(self, server_health: ServerHealth) -> ServerHealth:
        try:
            query, params = create_server_health_query(server_health)
            sql_query = SqlQuery(self.session, query, params)
            await sql_query.persist()
            return server_health
        except Exception as e:
            logger.error(f"Database error while saving server health for server {server_health.server_id}: {str(e)}", exc_info=True)
            raise RepositoryException("Failed to save server health")
        
    async def get_server_health(self, server_id: int) -> ServerHealth |None:
        try:
            query, params = get_server_health_query(server_id)
            sql_query = SqlQuery(self.session, query, params)
            server_helath = await sql_query.fetch_one(transformer=server_health_from_db)
            return server_helath
        except Exception as e:
            logger.error(f"Database error while fetching server health {server_id}: {str(e)}", exc_info=True)
            raise RepositoryException("Failed to retrieve server health")
        
    async def update_server_health(self, server_id, server_health: ServerHealth) -> ServerHealth:
        try:
            query, params = update_server_health_query(server_id, server_health)
            sql_query = SqlQuery(self.session, query, params)
            await sql_query.persist()
            return server_health
        except Exception as e:
            logger.error(f"Database error while updating server health {server_health.server_id}: {str(e)}", exc_info=True)
            raise RepositoryException("Failed to update server health")
        
    async def persist_server_health_history(self, server_history: ServerHistory) -> ServerHistory:
        try:
            query, params = create_health_history_query(server_history)
            sql_query = SqlQuery(self.session, query, params)
            await sql_query.persist()
            return server_history
        except Exception as e:
            logger.error(f"Database error while saving server health history for server {server_history.server_id}: {str(e)}", exc_info=True)
            raise RepositoryException("Failed to save server health")
        
    async def get_all_servers(self) -> list[Server]:
        try:
            query, params = get_all_servers_query()
            sql_query = SqlQuery(self.session, query, params)
            rows = await sql_query.fetch_all()
            servers =  [server_from_db(row) for row in rows]
            return [s for s in servers if s is not None]
        except Exception as e:
            logger.error(f"Database error while fetching all servers: {str(e)}", exc_info=True)
            raise RepositoryException("Failed to retrieve servers")