from typing import Any

from app.modules.server_health_ckeck.domain.entity.heallth_check import ServerCheck


def create_server_check_query(server_check: ServerCheck) -> tuple[str, dict[str, Any]]:
    query = """
    INSERT INTO server_checks (name, command, threshold, operator, unit, check_status)
    VALUES (:name, :command, :threshold, :operator, :unit, :check_status)
    RETURNING health_check_id
    """
    params = {
        "name": server_check.name,
        "command": server_check.command,
        "threshold": server_check.threshold,
        "operator": server_check.operator,
        "unit": server_check.unit,
        "check_status": server_check.check_status.value if hasattr(server_check.check_status, 'value') else server_check.check_status
    }
    return query, params


def get_server_checks_query() -> tuple[str, dict[str, Any]]:
    query = """
    SELECT health_check_id, name, command, threshold, operator, unit, check_status
    FROM server_checks
    ORDER BY health_check_id
    """
    params: dict[str, Any] = {}
    return query, params


def get_server_check_query(health_check_id: int) -> tuple[str, dict[str, Any]]:
    query = """
    SELECT health_check_id, name, command, threshold, operator, unit, check_status
    FROM server_checks
    WHERE health_check_id = :health_check_id
    """
    params = {"health_check_id": health_check_id}
    return query, params


def update_server_check_query(server_check: ServerCheck) -> tuple[str, dict[str, Any]]:
    query = """
    UPDATE server_checks
    SET name = :name,
        command = :command,
        threshold = :threshold,
        operator = :operator,
        unit = :unit,
        check_status = :check_status
    WHERE health_check_id = :health_check_id
    """
    params = {
        "health_check_id": server_check.health_check_id,
        "name": server_check.name,
        "command": server_check.command,
        "threshold": server_check.threshold,
        "operator": server_check.operator,
        "unit": server_check.unit,
        "check_status": server_check.check_status.value if hasattr(server_check.check_status, 'value') else server_check.check_status
    }
    return query, params


def delete_server_check_query(health_check_id: int) -> tuple[str, dict[str, Any]]:
    query = """
    DELETE FROM server_checks
    WHERE health_check_id = :health_check_id
    """
    params = {"health_check_id": health_check_id}
    return query, params
