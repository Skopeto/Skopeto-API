from fastapi import Depends
from app.core.dependencies import get_ssh_client
from app.modules.docker_registry.application.service.container_orchestration_service import (
    ContainerOrchestrationService,
    ContainerOrchestrationServiceInterface,
)
from app.modules.docker_registry.application.service.docker_metrics_service import DockerMetricService
from app.modules.docker_registry.domain.repository.docker_repository import DockerRepositoryInterface
from app.modules.docker_registry.infrastructure.sql_repository.docker_repository import SqlDockerRepository
from app.modules.server_registry.domain.repository.server_repository import ServerRepositoryInterface
from app.modules.server_registry.infrastructure.dependencies.dependencies import get_server_repository

from app.core.db_session import SessionDep


def get_docker_repository(session: SessionDep) -> DockerRepositoryInterface:
    return SqlDockerRepository(session)


def get_docker_metrics_service() -> DockerMetricService:
    return DockerMetricService(get_ssh_client())


def get_container_orchestration_service(
    server_repo: ServerRepositoryInterface = Depends(get_server_repository),
    docker_repo: DockerRepositoryInterface = Depends(get_docker_repository),
) -> ContainerOrchestrationServiceInterface:
    return ContainerOrchestrationService(
        server_repo=server_repo,
        docker_repo=docker_repo
    )