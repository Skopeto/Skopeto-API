import datetime
from typing import Any
from app.core.base_repository import SqlBaseRepository
from app.core.sql_query import SqlQuery
from app.modules.docker_registry.domain.entity.docker_container import DockerContainer
from app.modules.docker_registry.domain.repository.docker_repository import DockerRepositoryInterface
from app.modules.docker_registry.infrastructure.sql_query.docker_query import create_docker_container_query


class SqlDockerRepository(DockerRepositoryInterface, SqlBaseRepository):
    
    async def persist_docker_container(self, container: DockerContainer) -> DockerContainer:
        query, params = create_docker_container_query(container)
        sql_query = SqlQuery(self.session, query, params)
        await sql_query.persist()
        return container