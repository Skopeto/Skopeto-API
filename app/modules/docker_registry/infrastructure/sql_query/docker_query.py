from datetime import datetime
from typing import Any

from app.modules.docker_registry.domain.entity.docker_container import DockerContainer


def create_docker_container_query(container: DockerContainer) -> tuple[str, dict[str, Any]]:
    query = """
    INSERT INTO DOCKER_CONTAINERS (
        server_id,
        container_id
        name,
        image,
        status,
        ports,
        last_seen_at,
        created_at,
        updated_at,
    )
    VALUES (
        :server_id, :container_id, :name, :image, :status, :ports, :last_seen_at, :created_at, :updated_at
    )
    """
    
    params = {
        **container.model_dump()
    }
    return query, params