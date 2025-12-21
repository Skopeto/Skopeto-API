from datetime import datetime
from typing import Any


def get_user_q(user_id: int) -> tuple[str, dict[str, Any]]:
    query = "select u.* from fe_users u where user_id = :user_id"
    params = {
        'user_id': user_id  
    }

    return query, params

def get_user_by_token_q(token: str, now_time: datetime) -> tuple[str, dict[str, Any]]:
    query = """
    SELECT u.*
    FROM users u, access_tokens t
    WHERE t.access_token = :token
    AND t.is_valid = 1
    AND t.user_id = u.user_id
    """
    # AND t.date_expire >= :now_time
    params = {'token': token, 'now_time': now_time}
    return query, params


def get_user_by_username_password(user_name: str, password: str) -> tuple[str, dict[str, Any]]:
    query = """
    SELECT
    id,
    user_name,
    first_name,
    last_name,
    FROM USERS
    WHERE user_name = :user_name
    AND password = :password
    """
    params = {'user_name': user_name, 'password': password}
    return query, params