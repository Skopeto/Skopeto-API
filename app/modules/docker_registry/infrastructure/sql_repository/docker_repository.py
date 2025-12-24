import datetime
from typing import Any
from app.core.base_repository import SqlBaseRepository
from app.core.sql_query import SqlQuery
from app.modules.docker_registry.domain.repository.docker_repository import DockerRepositoryInterface

class SqlDockerRepository(DockerRepositoryInterface, SqlBaseRepository):
    async def persist_docker_container(): 