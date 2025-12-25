import datetime
from typing import Any
from app.core.base_repository import SqlBaseRepository
from app.core.sql_query import SqlQuery
from app.modules.server_registry.domain.entity.server import Server
from app.modules.server_registry.domain.entity.server_health import ServerHealth
from app.modules.server_registry.domain.entity.server_health import ServerHealth
from app.modules.server_registry.domain.repository.server_repository import ServerRepositoryInterface
from app.modules.server_registry.infrastructure.sql_query.server_query import create_server_query, create_server_health_query, get_server_query

def server_from_db(row: dict[str, Any] | None) -> Server:
    if not row:
        raise Exception('Server not found')
    server_attrs = {
        'id': row['user_id'],
        'registator_id': row['registator_id'],
        'user_name': row['user_name'],
        'password': row['password'],
        'ip_address': row['ip_address'],
        'port': row['port'],
        'status': row['status'],
    }
    return Server.model_construct(**server_attrs)

class SqlServerRepository(ServerRepositoryInterface, SqlBaseRepository):
    async def get_server(self, server_id: int) -> Server | None:
        query, params = get_server_query(server_id)
        sql_query = SqlQuery(self.session, query, params)
        return await sql_query.fetch_one(transformer=server_from_db)
    
    async def persist_server(self, server: Server) -> Server:
        query, params = create_server_query(server)
        sql_query = SqlQuery(self.session, query, params)
        await sql_query.persist()
        return server
    
    async def persist_server_health(self, server_health: ServerHealth) -> ServerHealth:
        query, params = create_server_health_query(server_health)
        sql_query = SqlQuery(self.session, query, params)
        await sql_query.persist()
        return server_health
        pass