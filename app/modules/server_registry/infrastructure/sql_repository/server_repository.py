from typing import Any
import logging
from app.core.Exception import RepositoryException
from app.core.base_repository import SqlBaseRepository
from app.core.sql_query import SqlQuery
from app.modules.server_registry.domain.entity.server import Server
from app.modules.server_registry.domain.entity.server_check_history import ServerCheckHistory
from app.modules.server_registry.domain.repository.server_repository import ServerRepositoryInterface
from app.modules.server_health_ckeck.domain.entity.heallth_check import ServerCheck
from app.modules.server_registry.infrastructure.sql_query.server_query import (
    create_server_check_history_query,
    create_server_query,
    delete_server_query,
    get_all_servers_query,
    get_server_query,
    update_server_query
)

logger = logging.getLogger(__name__)


def server_check_from_db(row: dict[str, Any]) -> ServerCheck:
    return ServerCheck.model_construct(
        health_check_id=row['health_check_id'],
        name=row['name'],
        command=row['command'],
        threshold=row['threshold'],
        operator=row['operator'],
        unit=row['unit'],
        check_status=row['check_status']
    )


def server_from_db(row: dict[str, Any] | None) -> Server | None:
    if not row:
        return None

    from app.modules.server_registry.domain.entity.server_status import ServerStatus

    server_attrs = {
        'id': row['id'],
        'user_name': row['user_name'],
        'ssh_password_encrypted': row['ssh_password_encrypted'],
        'ip_address': row['ip_address'],
        'port': row['port'],
        'status': ServerStatus(row['status']) if row['status'] else None,
    }
    return Server.model_construct(**server_attrs)


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

    async def persist_server_check_history(self, server_check_history: ServerCheckHistory) -> ServerCheckHistory:
        try:
            query, params = create_server_check_history_query(server_check_history)
            sql_query = SqlQuery(self.session, query, params)
            await sql_query.persist()
            return server_check_history
        except Exception as e:
            logger.error(f"Database error while saving server check history for server {server_check_history.server_id}: {str(e)}", exc_info=True)
            raise RepositoryException("Failed to save server check history")

    async def get_all_servers(self) -> list[Server]:
        try:
            query, params = get_all_servers_query()
            sql_query = SqlQuery(self.session, query, params)
            rows = await sql_query.fetch_all()
            servers = [server_from_db(row) for row in rows]
            return list(filter(None, servers))
        except Exception as e:
            logger.error(f"Database error while fetching all servers: {str(e)}", exc_info=True)
            raise RepositoryException("Failed to retrieve servers")

    async def delete_server(self, server_id: int) -> None:
        try:
            query, params = delete_server_query(server_id)
            await SqlQuery(self.session, query, params).delete()
        except Exception as e:
            logger.error(f"Database error while deleting server: {str(e)}", exc_info=True)
            raise RepositoryException("Failed to delete server")

    async def update_server(self, server: Server) -> Server:
        try:
            if server.id is None:
                raise RepositoryException("Server ID is required for update")

            query, params = update_server_query(server)
            await SqlQuery(self.session, query, params).persist()

            return server
        except Exception as e:
            logger.error(f"Database error while updating server: {str(e)}", exc_info=True)
            raise RepositoryException("Failed to update server")

    async def get_server_checks(self) -> list[ServerCheck]:
        try:
            query = """
                SELECT health_check_id, name, command, threshold, operator, unit, check_status
                FROM server_checks
                WHERE check_status = 'active'
                ORDER BY health_check_id
            """
            sql_query = SqlQuery(self.session, query, {})
            results = await sql_query.fetch_all()
            return [server_check_from_db(row) for row in results if row]
        except Exception as e:
            logger.error(f"Database error while fetching server checks: {str(e)}", exc_info=True)
            raise RepositoryException("Failed to retrieve server checks")
