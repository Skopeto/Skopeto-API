from typing import Any

from app.modules.database_registry.domain.entity.database import Database
from app.modules.database_registry.domain.entity.database_health import DatabaseHealth


def get_databases_query(server_id: int) -> tuple[str, dict[str, Any]]:
    query = """
    SELECT
        id,
        server_id,
        name,
        db_type,
        host,
        port,
        database_name,
        service_name,
        username,
        encrypted_password,
        created_at
    FROM databases
    WHERE server_id = :server_id
    """
    params: dict[str, Any] = {"server_id": server_id}
    return query, params


def create_database_query(database: Database) -> tuple[str, dict[str, Any]]:
    query = """
    INSERT INTO databases (
        server_id,
        name,
        db_type,
        host,
        port,
        database_name,
        service_name,
        username,
        encrypted_password,
        created_at
    )
    VALUES (
        :server_id,
        :name,
        :db_type,
        :host,
        :port,
        :database_name,
        :service_name,
        :username,
        :encrypted_password,
        :created_at
    )
    """
    params = {
        "server_id": database.server_id,
        "name": database.name,
        "db_type": database.db_type,
        "host": database.host,
        "port": database.port,
        "database_name": database.database_name,
        "service_name": database.service_name,
        "username": database.username,
        "encrypted_password": database.encrypted_password,
        "created_at": database.created_at.replace(tzinfo=None),
    }
    return query, params


def get_database_by_name_query(name: str) -> tuple[str, dict[str, Any]]:
    query = """
    SELECT
        id,
        server_id,
        name,
        db_type,
        host,
        port,
        database_name,
        service_name,
        username,
        encrypted_password,
        created_at
    FROM databases
    WHERE name = :name
    """
    params = {"name": name}
    return query, params


def create_database_health_query(
    database_health: DatabaseHealth,
) -> tuple[str, dict[str, Any]]:
    query = """
    INSERT INTO database_health (
        database_id,
        status,
        connection_time_ms,
        is_connected,
        query_time_ms,
        error_message,
        checked_at
    )
    VALUES (
        :database_id,
        :status,
        :connection_time_ms,
        :is_connected,
        :query_time_ms,
        :error_message,
        :checked_at
    )
    """
    params = {
        "database_id": database_health.database_id,
        "status": database_health.status.value,
        "connection_time_ms": database_health.connection_time_ms,
        "is_connected": database_health.is_connected,
        "query_time_ms": database_health.query_time_ms,
        "error_message": database_health.error_message,
        "checked_at": database_health.checked_at.replace(tzinfo=None)
        if database_health.checked_at
        else None,
    }
    return query, params


def get_database_health_query(database_id: int) -> tuple[str, dict[str, Any]]:
    query = """
    SELECT
        id,
        database_id,
        status,
        connection_time_ms,
        is_connected,
        query_time_ms,
        error_message,
        checked_at
    FROM database_health
    WHERE database_id = :database_id
    ORDER BY checked_at DESC
    LIMIT 1
    """
    params = {"database_id": database_id}
    return query, params


def update_database_health_query(
    database_health: DatabaseHealth,
) -> tuple[str, dict[str, Any]]:
    query = """
    UPDATE database_health
    SET
        status = :status,
        connection_time_ms = :connection_time_ms,
        is_connected = :is_connected,
        query_time_ms = :query_time_ms,
        error_message = :error_message,
        checked_at = :checked_at
    WHERE id = :id
    """
    params = {
        "id": database_health.id,
        "status": database_health.status.value,
        "connection_time_ms": database_health.connection_time_ms,
        "is_connected": database_health.is_connected,
        "query_time_ms": database_health.query_time_ms,
        "error_message": database_health.error_message,
        "checked_at": database_health.checked_at.replace(tzinfo=None)
        if database_health.checked_at
        else None,
    }
    return query, params


def update_database_query(database: Database) -> tuple[str, dict[str, Any]]:
    query = """
    UPDATE databases
    SET
        server_id = :server_id,
        name = :name,
        db_type = :db_type,
        host = :host,
        port = :port,
        database_name = :database_name,
        service_name = :service_name,
        username = :username,
        encrypted_password = :encrypted_password
    WHERE id = :id
    """
    params = {
        "id": database.id,
        "server_id": database.server_id,
        "name": database.name,
        "db_type": database.db_type,
        "host": database.host,
        "port": database.port,
        "database_name": database.database_name,
        "service_name": database.service_name,
        "username": database.username,
        "encrypted_password": database.encrypted_password,
    }
    return query, params


def get_database_by_id_query(id: int) -> tuple[str, dict[str, Any]]:
    query = """
    SELECT
        id,
        server_id,
        name,
        db_type,
        host,
        port,
        database_name,
        service_name,
        username,
        encrypted_password,
        created_at
    FROM databases
    WHERE id = :id
    """
    params = {"id": id}
    return query, params

def delete_database_query(database_id: int) -> tuple[str, dict]:
    query = """DELETE FROM databases WHERE id = :database_id"""
    params = {'database_id': database_id}
    return query, params
