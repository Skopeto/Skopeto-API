from fastapi import APIRouter, Depends, HTTPException
from app.modules.auth.domain.entity.user import User
from app.core.security import get_current_user
from app.modules.docker_registry.application.service.docker_metrics_service import DockerMetricService
from app.modules.docker_registry.application.use_case.collect_docker_container import collect_docker_container_data_use_case
from app.modules.docker_registry.domain.repository.docker_repository import DockerRepositoryInterface
from app.modules.docker_registry.infrastructure.dependencies.dependencies import get_docker_repository
from app.modules.server_registry.domain.entity.server import Server
from app.modules.server_registry.domain.repository.server_repository import ServerRepositoryInterface
from app.modules.server_registry.infrastructure.dependencies.dependencies import get_server_repository, get_ssh_client

router = APIRouter(prefix="/containers", tags=["Containers"])

@router.post("/get-container-data")
async def get_container_data(
    server_id: int,
    current_user: User = Depends(get_current_user),
    docker_repository: DockerRepositoryInterface = Depends(get_docker_repository),
    server_repository: ServerRepositoryInterface = Depends(get_server_repository),
    ssh_client: DockerMetricService = Depends(get_ssh_client)
):
    server_health = await collect_docker_container_data_use_case(server_id, ssh_client, server_repository, docker_repository)
    return server_health

