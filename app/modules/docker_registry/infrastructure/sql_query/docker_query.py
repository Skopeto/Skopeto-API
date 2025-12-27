from datetime import datetime
from typing import Any
from app.modules.docker_registry.domain.entity.docker_container import DockerContainer

def get_docker_container_query(name: str, server_id: int) -> tuple[str, dict[str, Any]]:
    query = """
        SELECT * FROM docker_containers 
        WHERE server_id = :server_id 
        AND name = :name
    """
    params = {"server_id": server_id, 'name': name}
    return query, params

def create_docker_container_query(container: DockerContainer) -> tuple[str, dict[str, Any]]:
    query = """
    INSERT INTO docker_containers (
        server_id,
        container_id,
        name,
        image,
        status,
        ports,
        exit_code,
        state_changed_at,
        is_healthy,
        last_seen_at
    )
    VALUES (
        :server_id, :container_id, :name, :image, :status, :ports,
        :exit_code, :state_changed_at, :is_healthy, CURRENT_TIMESTAMP
    )
    RETURNING id
    """
    params = {
        'server_id': container.server_id,
        'container_id': container.container_id,
        'name': container.name,
        'image': container.image,
        'status': container.status.value,
        'ports': container.ports,
        'exit_code': container.exit_code,
        'state_changed_at': container.state_changed_at.replace(tzinfo=None) if container.state_changed_at else None,
        'is_healthy': container.is_healthy
    }
    return query, params

def update_docker_container_query(container: DockerContainer) -> tuple[str, dict[str, Any]]:
    query = """
        UPDATE docker_containers
        SET
            container_id = :container_id,
            image = :image,
            status = :status,
            ports = :ports,
            exit_code = :exit_code,
            state_changed_at = :state_changed_at,
            is_healthy = :is_healthy,
            last_seen_at = CURRENT_TIMESTAMP,
            updated_at = CURRENT_TIMESTAMP
        WHERE name = :name
        AND server_id = :server_id
    """
    params = {
        'container_id': container.container_id,
        'server_id': container.server_id,
        'name': container.name,
        'image': container.image,
        'status': container.status.value,
        'ports': container.ports,
        'exit_code': container.exit_code,
        'state_changed_at': container.state_changed_at.replace(tzinfo=None) if container.state_changed_at else None,
        'is_healthy': container.is_healthy
    }
    return query, params

def get_docker_containers_query(server_id: int) -> tuple[str, dict[str, Any]]:
    query = "SELECT * FROM docker_containers WHERE server_id = :server_id"
    params = {"server_id": server_id}
    return query, params

def delete_duplicate_containers_query() -> tuple[str, dict[str, Any]]:
    query = """
        DELETE FROM docker_containers
        WHERE id IN (
            SELECT id FROM (
                SELECT id,
                    ROW_NUMBER() OVER (
                        PARTITION BY server_id, name
                        ORDER BY created_at DESC
                    ) as rn
                FROM docker_containers
            ) t
            WHERE t.rn > 1
        )
    """
    params = {}
    return query, params

def delete_all_containers_query() -> tuple[str, dict[str, Any]]:
    query = "DELETE FROM docker_containers"
    params = {}
    return query, params