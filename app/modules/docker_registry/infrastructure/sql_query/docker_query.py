from datetime import datetime
from typing import Any
from app.modules.docker_registry.domain.entity.docker_container import DockerContainer

def get_docker_container_query(container_id: str, server_id: int):
    query = """
        SELECT * FROM docker_containers 
        WHERE server_id = :server_id 
        AND container_id = :container_id
    """
    params = {"server_id": server_id, "container_id": container_id}
    return query, params

def create_docker_container_query(container: DockerContainer) -> tuple[str, dict[str, Any]]:
    query = """
    INSERT INTO docker_containers (
        server_id,
        container_id,
        name,
        image,
        status,
        ports
    )
    VALUES (
        :server_id, :container_id, :name, :image, :status, :ports
    )
    RETURNING id
    """
    params = {
        'server_id': container.server_id,
        'container_id': container.container_id,
        'name': container.name,
        'image': container.image,
        'status': container.status.value,
        'ports': container.ports
    }
    return query, params

def update_docker_container_query(container: DockerContainer) -> tuple[str, dict[str, Any]]:
    query = """
        UPDATE docker_containers
        SET
            name = :name,
            image = :image,
            status = :status,
            ports = :ports,
            last_seen_at = CURRENT_TIMESTAMP
        WHERE container_id = :container_id 
        AND server_id = :server_id
    """
    params = {
        'container_id': container.container_id,
        'server_id': container.server_id,
        'name': container.name,
        'image': container.image,
        'status': container.status.value,
        'ports': container.ports
    }
    return query, params