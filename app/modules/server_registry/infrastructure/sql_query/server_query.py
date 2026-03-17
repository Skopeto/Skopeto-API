from typing import Any

from app.modules.server_registry.domain.entity.server import Server
from app.modules.server_registry.domain.entity.server_check_results import ServerCheckResults
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

def create_server_check_results_query(server_check_results: ServerCheckResults) -> tuple[str, dict[str, Any]]:
    query = """
    INSERT INTO server_check_results (
        server_id,
        status,
        check_name,
        unit,
        uptime,
        checked_at
    )
    VALUES (
        :server_id, :status, :check_name, :unit, :uptime, :checked_at
    )
    """
    params = {
        'server_id': server_check_results.server_id,
        'status': server_check_results.status.value,
        'check_name': server_check_results.check_name,
        'unit': server_check_results.unit,
        'uptime': server_check_results.uptime,
        'checked_at': server_check_results.checked_at.replace(tzinfo=None) if server_check_results.checked_at else None
    }
    return query, params

def update_server_check_results_query(server_id: int, server_check_results: ServerCheckResults) -> tuple[str, dict[str, Any]]:
    query = """
        UPDATE server_check_results
        SET
            status = :status,
            check_name = :check_name,
            unit = :unit,
            uptime = :uptime,
            checked_at = :checked_at
        WHERE server_id = :server_id
    """
    params = {
        'server_id': server_id,
        'status': server_check_results.status.value,
        'check_name': server_check_results.check_name,
        'unit': server_check_results.unit,
        'uptime': server_check_results.uptime,
        'checked_at': server_check_results.checked_at.replace(tzinfo=None) if server_check_results.checked_at else None
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
        'checked_at': server_history.checked_at.replace(tzinfo=None) if server_history.checked_at else None
    }
    return query, params

def get_all_servers_query() -> tuple[str, dict[str, Any]]:
    query = """
        SELECT * FROM servers
    """
    params = {}
    return query, params

def delete_server_query(server_id: int) -> tuple[str, dict]:
    query = """DELETE FROM servers WHERE id = :server_id"""
    params = {'server_id': server_id}
    return query, params

def update_server_query(server: Server) -> tuple[str, dict]:
    query = """
        UPDATE servers
        SET
            user_name = :user_name,
            ssh_password_encrypted = :ssh_password_encrypted,
            ip_address = :ip_address,
            port = :port,
            status = :status
        WHERE id = :id
    """
    params = {
        'id': server.id,
        'user_name': server.user_name,
        'ssh_password_encrypted': server.ssh_password_encrypted,
        'ip_address': server.ip_address,
        'port': server.port,
        'status': server.status.value if server.status else None
    }
    return query, params