from datetime import datetime
from typing import Any

from app.modules.server_registry.domain.entity.server import Server
from app.modules.server_registry.domain.entity.server_health import ServerHealth
from app.modules.server_registry.domain.entity.server_history import ServerHistory

def get_server_query(server_id: int) -> tuple[str, dict[str, Any]]:
    query = "select s.* from servers s where id = :id"
    params = {
        'id': server_id  
    }
    return query, params

def get_server_health_query(server_id: int) -> tuple[str, dict[str, Any]]:
    query = "select s.* from server_health s where server_id = :server_id"
    params = {
        'server_id': server_id  
    }
    return query, params

def create_server_query(server: Server) -> tuple[str, dict[str, Any]]:
    query = """
        INSERT INTO servers (
            user_name,
            ssh_password_encrypted,
            ip_address,
            port,
            status
        )
        VALUES (
             :user_name, :ssh_password_encrypted, :ip_address, :port, :status
        )
        RETURNING id
        """
    params = {
            'user_name': server.user_name,
            'ssh_password_encrypted': server.ssh_password_encrypted,
            'ip_address': server.ip_address,
            'port': server.port,
            'status': server.status
        }
    return query, params

def create_server_health_query(server_health: ServerHealth) -> tuple[str, dict[str, Any]]:
    query = """
    INSERT INTO server_health (
        server_id,
        status,
        cpu_usage,
        memory_usage,
        disk_usage,
        uptime,
        checked_at
    )
    VALUES (
        :server_id, :status, :cpu_usage, :memory_usage, :disk_usage, :uptime, :checked_at
    )
    """
    params = {
        'server_id': server_health.server_id,
        'status': server_health.status.value,
        'cpu_usage': server_health.cpu_usage,
        'memory_usage': server_health.memory_usage,
        'disk_usage': server_health.disk_usage,
        'uptime': server_health.uptime,
        'checked_at': server_health.checked_at
    }
    return query, params

def update_server_health_query(server_id: int, server_health: ServerHealth) -> tuple[str, dict[str, Any]]:
    query = """
        UPDATE server_health
        SET
            status = :status,
            cpu_usage = :cpu_usage,
            memory_usage = :memory_usage,
            disk_usage = :disk_usage,
            uptime = :uptime,
            checked_at = :checked_at
        WHERE server_id = :server_id
    """
    params = {
        'server_id': server_id,
        'status': server_health.status.value,
        'cpu_usage': server_health.cpu_usage,
        'memory_usage': server_health.memory_usage,
        'disk_usage': server_health.disk_usage,
        'uptime': server_health.uptime,
        'checked_at': server_health.checked_at
    }
    return query, params

def create_health_history_query(server_history: ServerHistory) -> tuple[str, dict[str, Any]]:
    query = """
    INSERT INTO server_history (
        server_id,
        status,
        cpu_usage,
        memory_usage,
        disk_usage,
        uptime,
        checked_at
    )
    VALUES (
        :server_id, :status, :cpu_usage, :memory_usage, :disk_usage, :uptime, :checked_at
    )
    """
    params = {
        'server_id': server_history.server_id,
        'status': server_history.status.value,
        'cpu_usage': server_history.cpu_usage,
        'memory_usage': server_history.memory_usage,
        'disk_usage': server_history.disk_usage,
        'uptime': server_history.uptime,
        'checked_at': server_history.checked_at
    }
    return query, params

def get_all_servers_query() -> tuple[str, dict[str, Any]]:
    query = """
        SELECT * FROM servers
    """
    params = {}
    return query, params

