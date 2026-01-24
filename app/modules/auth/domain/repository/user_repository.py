from abc import ABC, abstractmethod
from typing import Optional
from app.modules.auth.domain.entity.user import User

class UserRepositoryInterface(ABC):
    @abstractmethod
    async def persist_user(self, user: User) -> User:
        raise NotImplementedError()
    
    @abstractmethod
    async def get_by_username(self, username: str) -> User:
        raise NotImplementedError()
    
    @abstractmethod
    async def get_user_by_token(self, token: str) -> Optional[User]:
        raise NotImplementedError()
    
    @abstractmethod
    async def get_user(self, user_id: int) -> Optional[User]:
        raise NotImplementedError()
    
    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[User]:
        raise NotImplementedError()
    
    @abstractmethod
    async def get_users(self) -> list[User] | None:
        raise NotImplementedError()
    
    @abstractmethod
    async def update_user(self, user: User) -> User:
        raise NotImplementedError()