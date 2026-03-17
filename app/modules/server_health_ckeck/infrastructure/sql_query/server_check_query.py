from typing import Any

from app.modules.server_health_ckeck.domain.entity.heallth_check import ServerCheck

def create_server_check_query(server_check: ServerCheck)->tuple[str, dict[str, Any]]:
        query = """
        INSERT INTO server_checks (health_check_id, name, command, threshold, operator, unit, check_status)
        VALUES (:health_check_id, :name, :command, :threshold, :operator, :unit, :check_status)
        """
        params = {
            "health_check_id": server_check.health_check_id,
            "name": server_check.name,
            "command": server_check.command,
            "threshold": server_check.threshold,
            "operator": server_check.operator,
            "unit": server_check.unit,
            "check_status": server_check.check_status
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
