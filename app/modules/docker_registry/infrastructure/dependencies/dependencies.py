from app.core.dependencies import get_ssh_client
from app.modules.docker_registry.application.service.docker_metrics_service import DockerMetricService
from app.modules.docker_registry.domain.repository.docker_repository import DockerRepositoryInterface
from app.modules.docker_registry.infrastructure.sql_repository.docker_repository import SqlDockerRepository

from app.core.db_session import SessionDep

def get_docker_repository(session: SessionDep) -> DockerRepositoryInterface:
    return SqlDockerRepository(session)

def get_docker_metrics_service() -> DockerMetricService:
    return DockerMetricService(get_ssh_client())