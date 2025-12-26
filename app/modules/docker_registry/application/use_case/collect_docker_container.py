from datetime import datetime, timezone
from app.core.Exception import ApplicationException
from app.modules.docker_registry.application.service.docker_metrics_service import DockerMetricService
from app.modules.docker_registry.domain.entity.docker_container import DockerContainer
from app.modules.docker_registry.domain.repository.docker_repository import DockerRepositoryInterface
from app.modules.server_registry.domain.repository.server_repository import ServerRepositoryInterface

async def collect_docker_container_data_use_case(
    server_id: int,
    docker_service: DockerMetricService,
    server_repository: ServerRepositoryInterface,
    docker_repository: DockerRepositoryInterface
) -> list[DockerContainer]:

    server = await server_repository.get_server(server_id)

    if not server:
        raise ApplicationException(f"Server {server_id} not found")

    docker_container_data = await docker_service.get_docker_metrics(server)

    if not docker_container_data:
        raise ApplicationException(f"No containers found on server {server_id}")

    persisted_containers = []

    for data in docker_container_data:
        container = DockerContainer(**data)

        existing = await docker_repository.get_docker_container(container.container_id, server_id)

        if existing and existing.status != container.status:
            container.state_changed_at = datetime.now(timezone.utc)
        elif not existing:
            container.state_changed_at = datetime.now(timezone.utc)

        if existing:
            persisted = await docker_repository.update_docker_container(container)
        else:
            persisted = await docker_repository.persist_docker_container(container)

        persisted_containers.append(persisted)

    return persisted_containers
