
import logging
from app.core.Exception import RepositoryException
from app.core.base_repository import SqlBaseRepository
from app.core.sql_query import SqlQuery
from app.modules.server_health_ckeck.domain.repository.server_check_repository_interface import ServerCheckRepositoryInterface
from app.modules.server_health_ckeck.infrastructure.sql_query.server_check_query import create_server_check_query
logger = logging.getLogger(__name__)

class SqlServerCheckRepository(ServerCheckRepositoryInterface, SqlBaseRepository):
    async def create_server_check(self, server_check) -> None:
        try:
            query, params = create_server_check_query(server_check)
            sql_query = SqlQuery(self.session, query, params)
            await sql_query.persist()
        except Exception as e:
            logger.error(f"Error creating server check: {str(e)}")
            raise RepositoryException(f"Failed to create server check: {str(e)}") from e
