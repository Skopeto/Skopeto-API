from typing import Any

def get_timer_query() -> tuple[str, dict[str, Any]]:
    query = """
        SELECT id, interval_minutes, created_at
        FROM scheduler_timer
        ORDER BY created_at DESC, id DESC
        LIMIT 1
    """
    return query, {}

def update_timer_query(interval_minutes: int) -> tuple[str, dict[str, Any]]:
    query = """
        UPDATE scheduler_timer
        SET interval_minutes = :interval_minutes
        WHERE id = (
            SELECT id FROM scheduler_timer
            ORDER BY created_at DESC, id DESC
            LIMIT 1
        )
    """
    return query, {'interval_minutes': interval_minutes}

def create_timer_query(interval_minutes: int) -> tuple[str, dict[str, Any]]:
    query = """
        INSERT INTO scheduler_timer (interval_minutes)
        VALUES (:interval_minutes)
    """
    return query, {'interval_minutes': interval_minutes}