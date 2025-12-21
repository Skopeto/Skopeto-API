from abc import ABC,abstractmethod
from typing import Optional
from app.modules.auth.domain.entity.user import User

class UserRepositoryInterface(ABC):

    @abstractmethod
    def get_by_username_or_email(self, username: str, email: str) -> Optional[User]:
        raise NotImplementedError()

    @abstractmethod
    def persist(self, user: User) -> User:
        raise NotImplementedError()