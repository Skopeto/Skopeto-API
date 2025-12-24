from datetime import datetime
from typing import Any

from app.modules.server_registry.domain.entity.server import Server
from app.modules.server_registry.domain.entity.server_health import ServerHealth

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