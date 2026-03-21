from datetime import datetime, timezone
import logging
from app.modules.docker_registry.application.service.docker_metrics_service import DockerMetricService
from app.modules.docker_registry.domain.entity.docker_container import DockerContainer
from app.modules.docker_registry.domain.repository.docker_repository import DockerRepositoryInterface
from app.modules.server_registry.domain.entity.server import Server
from app.modules.server_registry.domain.entity.server_check_results import HealthStatus, ServerCheckResults

logger = logging.getLogger(__name__)


def is_server_reachable(check_results: list[ServerCheckResults]) -> bool:
    """Check if server is reachable based on check results.
    Server is reachable if no checks returned OFFLINE or ERROR status.
    """
    if not check_results:
        return False
    return all(
        result.status not in (HealthStatus.OFFLINE, HealthStatus.ERROR)
        for result in check_results
    )


async def collect_container_metrics_use_case(
    server_id: int,
    server: Server,
    server_check_results: list[ServerCheckResults],
    docker_repository: DockerRepositoryInterface,
    docker_metrics_service: DockerMetricService
) -> list[DockerContainer]:

    containers = []

    if not is_server_reachable(server_check_results):
        return containers

    try:
        docker_data = await docker_metrics_service.get_docker_metrics(server)

        for container_data in docker_data:
            container = DockerContainer(**container_data)

            existing_container = await docker_repository.get_docker_container(
                container.name,
                server_id
            )

            if existing_container and existing_container.status != container.status:
                container.state_changed_at = datetime.now(timezone.utc)
            elif not existing_container:
                container.state_changed_at = datetime.now(timezone.utc)

            if existing_container:
                persisted = await docker_repository.update_docker_container(container)
            else:
                persisted = await docker_repository.persist_docker_container(container)

            containers.append(persisted)
    except Exception as e:
        logger.error(f"Failed to collect containers for {server.ip_address}: {e}", exc_info=True)

    return containers
