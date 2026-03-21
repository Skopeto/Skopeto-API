import logging
from typing import Any
from app.core.Exception import RepositoryException
from app.core.base_repository import SqlBaseRepository
from app.core.sql_query import SqlQuery
from app.modules.server_health_ckeck.domain.entity.heallth_check import ServerCheck
from app.modules.server_health_ckeck.domain.repository.server_check_repository_interface import ServerCheckRepositoryInterface
from app.modules.server_health_ckeck.infrastructure.sql_query.server_check_query import (
    create_server_check_query,
    get_server_checks_query,
    get_server_check_query,
    update_server_check_query,
    delete_server_check_query
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


class SqlServerCheckRepository(ServerCheckRepositoryInterface, SqlBaseRepository):

    async def create_server_check(self, server_check: ServerCheck) -> None:
        try:
            query, params = create_server_check_query(server_check)
            sql_query = SqlQuery(self.session, query, params)
            await sql_query.persist()
        except Exception as e:
            logger.error(f"Error creating server check: {str(e)}")
            raise RepositoryException(f"Failed to create server check: {str(e)}") from e

    async def get_server_checks(self) -> list[ServerCheck]:
        try:
            query, params = get_server_checks_query()
            sql_query = SqlQuery(self.session, query, params)
            results = await sql_query.fetch_all()
            server_checks = [server_check_from_db(row) for row in results if row]
            return server_checks
        except Exception as e:
            logger.error(f"Error fetching server checks: {str(e)}")
            raise RepositoryException(f"Failed to fetch server checks: {str(e)}") from e

    async def get_server_check(self, health_check_id: int) -> ServerCheck | None:
        try:
            query, params = get_server_check_query(health_check_id)
            sql_query = SqlQuery(self.session, query, params)
            result = await sql_query.fetch_one(transformer=server_check_from_db)
            return result
        except Exception as e:
            logger.error(f"Error fetching server check {health_check_id}: {str(e)}")
            raise RepositoryException(f"Failed to fetch server check: {str(e)}") from e

    async def update_server_check(self, server_check: ServerCheck) -> ServerCheck:
        try:
            query, params = update_server_check_query(server_check)
            sql_query = SqlQuery(self.session, query, params)
            await sql_query.persist()
            return server_check
        except Exception as e:
            logger.error(f"Error updating server check {server_check.health_check_id}: {str(e)}")
            raise RepositoryException(f"Failed to update server check: {str(e)}") from e

    async def delete_server_check(self, health_check_id: int) -> None:
        try:
            query, params = delete_server_check_query(health_check_id)
            sql_query = SqlQuery(self.session, query, params)
            await sql_query.delete()
        except Exception as e:
            logger.error(f"Error deleting server check {health_check_id}: {str(e)}")
            raise RepositoryException(f"Failed to delete server check: {str(e)}") from e
