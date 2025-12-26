from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.modules.auth.domain.entity.user import User
from app.core.security import get_current_user
from app.modules.docker_registry.application.service.docker_metrics_service import DockerMetricService
from app.modules.docker_registry.application.use_case.collect_docker_container import collect_docker_container_data_use_case
from app.modules.docker_registry.domain.repository.docker_repository import DockerRepositoryInterface
from app.modules.docker_registry.infrastructure.dependencies.dependencies import get_docker_metrics_service, get_docker_repository
from app.modules.server_registry.domain.repository.server_repository import ServerRepositoryInterface
from app.modules.server_registry.infrastructure.dependencies.dependencies import get_server_repository

router = APIRouter(prefix="/containers", tags=["Containers"])

class ContainerDataRequest(BaseModel):
    server_id: int

@router.post("/get-container-data")
async def get_container_data(
    request: ContainerDataRequest,
    current_user: User = Depends(get_current_user),
    docker_repository: DockerRepositoryInterface = Depends(get_docker_repository),
    server_repository: ServerRepositoryInterface = Depends(get_server_repository),
    ssh_client: DockerMetricService = Depends(get_docker_metrics_service)
):
    containers = await collect_docker_container_data_use_case(
        request.server_id,
        ssh_client,
        server_repository,
        docker_repository
    )
    return {"status": "success", "data": containers}