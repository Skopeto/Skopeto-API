from fastapi import APIRouter, Depends, HTTPException
from app.core.dependencies import get_ssh_client
from app.core.ssh_client import SSHClientInterface
from app.modules.auth.domain.entity.user import User
from app.core.security import get_current_user
from app.modules.docker_registry.domain.repository.docker_repository import DockerRepositoryInterface
from app.modules.server_registry.application.use_case.collect_server_health import collect_server_health_use_case
from app.modules.server_registry.domain.repository.server_repository import ServerRepositoryInterface
from app.modules.server_registry.infrastructure.dependencies.dependencies import get_server_repository

router = APIRouter(prefix="/metrics", tags=["Metrics"])

@router.get("/servers/containers/{server_id}")
async def get_server_health(
    server_id: int,
    current_user: User = Depends(get_current_user),
    server_repository: ServerRepositoryInterface = Depends(get_server_repository),
    docker_repository: DockerRepositoryInterface = Depends(get_docker_repository)
    ssh_client: SSHClientInterface = Depends(get_ssh_client)
):
    server_health = await collect_server_health_use_case(server_id, server_repository, ssh_client)
