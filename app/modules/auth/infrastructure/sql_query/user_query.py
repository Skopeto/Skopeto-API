from datetime import datetime
from typing import Any

from app.modules.auth.domain.entity.user import User

def get_user_query(user_id: int) -> tuple[str, dict[str, Any]]:
    query = "select u.* from users u where id = :user_id"
    params = {
        'user_id': user_id  
    }
    return query, params

def get_user_by_token_query(token: str, now_time: datetime) -> tuple[str, dict[str, Any]]:
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

def get_user_by_username_query(user_name: str) -> tuple[str, dict[str, Any]]:
    query = """
    SELECT
        id,
        user_name,
        first_name,
        last_name,
        email,
        hashed_password,
        roles
    FROM users
    WHERE user_name = :user_name
    """
    params = {'user_name': user_name}
    return query, params


def create_user_query(user: User) -> tuple[str, dict[str, Any]]:
    query = """
    INSERT INTO users (
        user_name,
        first_name,
        last_name,
        email,
        hashed_password,
        roles,
        is_active,
        is_superuser
    )
    VALUES (
        :user_name, :first_name, :last_name, :email, :hashed_password, :roles, :is_active, :is_superuser
    )
    """
    
    params = {
        **user.model_dump(),
        'roles': ','.join([role.value for role in user.roles])
    }
    
    return query, params

def get_user_by_email_query( email: str) -> tuple[str, dict[str, Any]]:
    query = """
    SELECT *
    FROM USERS
    WHERE user_name = :username
    OR email = :email
    """
    params = {'email': email}
    return query, params 

def get_users_query() -> tuple[str, dict[str, Any]]:
    query = """
    SELECT *
    FROM users
    """
    params = {}
    return query, params

def update_user_query(user: User) -> tuple[str, dict[str, Any]]:
    query = """
    UPDATE users
    SET
        user_name = :user_name,
        first_name = :first_name,
        last_name = :last_name,
        email = :email,
        hashed_password = :hashed_password,
        roles = :roles,
        is_active = :is_active,
        is_superuser = :is_superuser
    WHERE id = :id
    """
    params = {
        **user.model_dump(),
        'roles': ','.join([role.value for role in user.roles])
    }
    return query, params