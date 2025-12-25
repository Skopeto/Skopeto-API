from datetime import datetime
from typing import Any

from app.modules.server_registry.domain.entity.server import Server
from app.modules.server_registry.domain.entity.server_health import ServerHealth
from app.modules.server_registry.domain.entity.server_history import ServerHistory

def get_server_query(server_id: int) -> tuple[str, dict[str, Any]]:
    query = "select s.* from servers s where server_id = :server_id"
    params = {
        'server_id': server_id  
    }
    return query, params

def create_server_query(server: Server) -> tuple[str, dict[str, Any]]:
    query = """
    INSERT INTO SERVERS (
        registator_id,
        name,
        password,
        ip_address,
        port,
        status
    )
    VALUES (
        :registator_id, :name, :password, :ip_address, :port, :status
    )
    """
    
    params = {
        **server.model_dump()
    }
    return query, params


def create_server_health_query(server_health: ServerHealth) -> tuple[str, dict[str, Any]]:
    query = """
    INSERT INTO SERVER_HEALTH (
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
        **server_health.model_dump()
    }
    return query, params

def update_server_health_query(server_health: ServerHealth) -> tuple[str, dict[str, Any]]:
    query = """
        UPDATE SERVER_HEALTH
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
        'server_id': server_health.server_id,
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
    INSERT INTO SERVER_HEALTH_HISTORY (
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
        **server_history.model_dump()
    }
    return query, params

def get_all_servers_query() -> tuple[str, dict[str, Any]]:
    query = """
        SELECT * FROM servers
    """
    params = {}
    return query, params

