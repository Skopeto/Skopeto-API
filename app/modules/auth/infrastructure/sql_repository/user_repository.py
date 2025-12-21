import datetime
from typing import Any
from app.core.base_repository import SqlBaseRepository
from app.core.sql_query import SqlQuery
from app.modules.auth.domain.entity.user import User
from app.modules.auth.domain.repository.user_repository import UserRepositoryInterface
from app.modules.auth.infrastructure.sql_query.user_query import create_user_query, get_user_by_username_password_query, get_user_query
from app.modules.auth.infrastructure.sql_query.user_query import get_user_by_token_query, get_user_by_username_or_email_query

def user_from_db(row: dict[str, Any] | None) -> User:
    if not row:
        raise Exception('user not found')
    user_attrs = {
        'id': row['user_id'],
        'username': row['user_name'],
    }
    return User.model_construct(**user_attrs)

class SqlUserRepository(UserRepositoryInterface, SqlBaseRepository):
    async def get_user(self, user_id: int) -> User | None:
        query, params = get_user_query(user_id)
        sql_query = SqlQuery(self.session, query, params)
        return await sql_query.fetch_one(transformer=user_from_db)
    
    async def get_user_by_token(self, token: str) -> User | None:
        query, params = get_user_by_token_query(token, now_time=datetime.datetime.now())
        sql_query = SqlQuery(self.session, query, params)
        return await sql_query.fetch_one(transformer=user_from_db)
    
    async def persist_user(self, user: User) -> User:
        query, params = create_user_query(user)
        sql_query = SqlQuery(self.session, query, params)
        await sql_query.persist()
        return user

    async def get_by_username(self, username: str) -> User | None:
        query, params = get_user_by_username_password_query(username)
        sql_query = SqlQuery(self.session, query, params)
        return await sql_query.fetch_one(transformer=user_from_db)
    
    async def get_by_username_or_email(self, username: str, email: str) -> User | None:
        query, params = get_user_by_username_or_email_query(username, email)
        sql_query = SqlQuery(self.session, query, params)
        return await sql_query.fetch_one(transformer=user_from_db)