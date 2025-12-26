import datetime
from typing import Any
import logging
from app.core.Exception import RepositoryException
from app.core.base_repository import SqlBaseRepository
from app.core.sql_query import SqlQuery
from app.modules.docker_registry.domain.entity.docker_container import DockerContainer
from app.modules.docker_registry.domain.repository.docker_repository import DockerRepositoryInterface
from app.modules.docker_registry.infrastructure.sql_query.docker_query import create_docker_container_query, get_docker_container_query, update_docker_container_query
logger = logging.getLogger(__name__)

def container_from_db(row: dict[str, Any] | None) -> DockerContainer | None:
    if not row:
        return None
    
    container_attrs = {
        'id': row['id'],
        'server_id': row['server_id'],
        'container_id': row['container_id'],
        'name': row['name'],
        'image': row['image'],
        'status': row['status'],
        'ports': row['ports'],
        'exit_code': row.get('exit_code'),
        'state_changed_at': row.get('state_changed_at'),
        'is_healthy': row.get('is_healthy'),
        'last_seen_at': row['last_seen_at'],
        'created_at': row['created_at'],
        'updated_at': row['updated_at'],
    }
    return DockerContainer.model_construct(**container_attrs)

class SqlDockerRepository(DockerRepositoryInterface, SqlBaseRepository):

    async def get_docker_container(self, container_id: str, server_id: int) -> DockerContainer | None:
        try:
            query, params = get_docker_container_query(container_id, server_id)
            sql_query = SqlQuery(self.session, query, params)
            row = await sql_query.fetch_one(transformer=container_from_db)
            return row
        except Exception as e:
            logger.error(f"Database error while fetching container: {str(e)}", exc_info=True)
            raise RepositoryException("Failed to fetch container")
    
    async def persist_docker_container(self, container: DockerContainer) -> DockerContainer:
        try:
            query, params = create_docker_container_query(container)
            sql_query = SqlQuery(self.session, query, params)
            await sql_query.persist()
            return container
        except Exception as e:
            logger.error(f"Database error while saving container: {str(e)}", exc_info=True)
            raise RepositoryException("Failed to save container")
        
    async def update_docker_container(self, container: DockerContainer) -> DockerContainer:
        try:
            query, params = update_docker_container_query(container)
            sql_query = SqlQuery(self.session, query, params)
            await sql_query.persist()
            return container
        except Exception as e:
            logger.error(f"Database error while saving container: {str(e)}", exc_info=True)
            raise RepositoryException("Failed to save container")