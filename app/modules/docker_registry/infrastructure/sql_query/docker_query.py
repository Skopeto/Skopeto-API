from datetime import datetime
from typing import Any
from app.modules.docker_registry.domain.entity.docker_container import DockerContainer

def get_docker_container_query(container_id: str, server_id: int) -> tuple[str, dict[str, Any]]:
    query = "select s.* from docker_containers dc where server_id = :server_id and where container_id = :container_id"
    params = {
        'server_id': server_id,
        'container_id': container_id
    }
    return query, params

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

def update_docker_container_query(container: DockerContainer) -> tuple[str, dict[str, Any]]:
    query = """
        UPDATE SERVER_HEALTH
        SET
            server_id = :server_id,
            status = :status,
            name = :name,
            image = :image,
            status = :status,
            ports = :ports,
            last_seen_at= :last_seen_at,
            created_at= :last_seen_at,
            updated_at= :last_seen_at,
        WHERE server_id = :server_id
    """
    params = {
        'server_id': container.server_id,
        'status': container.status.value,
        'name': container.name,
        'image': container.image,
        'status': container.status,
        'ports': container.ports,
        'last_seen_at': container.last_seen_at,
        'created_at': container.created_at,
        'updated_at': container.updated_at
    }
    return query, params