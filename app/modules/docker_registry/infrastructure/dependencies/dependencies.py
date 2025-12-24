from app.core.dependencies import get_ssh_client
from app.modules.docker_registry.domain.repository.docker_repository import DockerRepositoryInterface
from app.modules.docker_registry.infrastructure.sql_repository.docker_repository import SqlDockerRepository
from app.modules.server_registry.application.service.server_metrics_service import ServerMetricsService
from app.core.db_session import SessionDep

def get_docker_repository(session: SessionDep) -> DockerRepositoryInterface:
    return SqlDockerRepository(session)