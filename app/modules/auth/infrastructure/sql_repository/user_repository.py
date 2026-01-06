import datetime
from typing import Any
import logging
import json
from app.core.Exception import RepositoryException
from app.core.base_repository import SqlBaseRepository
from app.core.sql_query import SqlQuery
from app.modules.auth.domain.entity.user import Roles, User
from app.modules.auth.domain.repository.user_repository import UserRepositoryInterface
from app.modules.auth.infrastructure.sql_query.user_query import (
    create_user_query,
    get_user_by_username_query,
    get_user_query,
    get_user_by_token_query,
    get_user_by_username_or_email_query,
    get_users_query
)

logger = logging.getLogger(__name__)

def user_from_db(row: dict[str, Any] | None) -> User | None:
    if not row:
        return None
    
    roles_data = row.get('roles', [])
    if isinstance(roles_data, str):
        try:
            roles_data = json.loads(roles_data)
        except:
            roles_data = [roles_data]
    
    roles = [Roles(r) if isinstance(r, str) else r for r in roles_data]
    
    user_attrs = {
        'id': row['id'],
        'user_name': row['user_name'],
        'first_name': row.get('first_name'),
        'last_name': row.get('last_name'),
        'email': row['email'],
        'hashed_password': row['hashed_password'],
        'roles': roles,
    }
    
    return User.model_construct(**user_attrs)

class SqlUserRepository(UserRepositoryInterface, SqlBaseRepository):
    async def get_user(self, user_id: int) -> User | None:
        try:
            query, params = get_user_query(user_id)
            sql_query = SqlQuery(self.session, query, params)
            user = await sql_query.fetch_one(transformer=user_from_db)
            return user
        except Exception as e:
            logger.error(f"Database error while fetching user {user_id}: {str(e)}", exc_info=True)
            raise RepositoryException("Failed to retrieve user")
    
    async def get_user_by_token(self, token: str) -> User | None:
        try:
            query, params = get_user_by_token_query(token, now_time=datetime.datetime.now())
            sql_query = SqlQuery(self.session, query, params)
            user = await sql_query.fetch_one(transformer=user_from_db)
            return user
        except Exception as e:
            logger.error(f"Database error while fetching user by token: {str(e)}", exc_info=True)
            raise RepositoryException("Failed to retrieve user")
    
    async def persist_user(self, user: User) -> User:
        try:
            query, params = create_user_query(user)
            sql_query = SqlQuery(self.session, query, params)
            await sql_query.persist()
            return user
        except Exception as e:
            logger.error(f"Database error while saving user {user.id}: {str(e)}", exc_info=True)
            raise RepositoryException('Failed to save user')
    
    async def get_by_username(self, username: str) -> User | None:
        try:
            query, params = get_user_by_username_query(username)
            sql_query = SqlQuery(self.session, query, params)
            user = await sql_query.fetch_one(transformer=user_from_db)
            return user
        except Exception as e:
            logger.error(f"Database error while fetching user by username '{username}': {str(e)}", exc_info=True)
            raise RepositoryException("Failed to retrieve user")
    
    async def get_by_username_or_email(self, username: str, email: str) -> User | None:
        try:
            query, params = get_user_by_username_or_email_query(username, email)
            sql_query = SqlQuery(self.session, query, params)
            user = await sql_query.fetch_one(transformer=user_from_db)
            return user
        except Exception as e:
            logger.error(f"Database error while checking username/email: {str(e)}", exc_info=True)
            raise RepositoryException("Failed to check user existence")
        
    async def get_users(self) -> list[User | None]:
        try:
            query, params = get_users_query()
            sql_query = SqlQuery(self.session, query, params)
            users = await sql_query.fetch_all(transformer=user_from_db)
            return users
        except Exception as e:
            logger.error(f"Database error while fetching users: {str(e)}", exc_info=True)
            raise RepositoryException("Failed to retrieve users")