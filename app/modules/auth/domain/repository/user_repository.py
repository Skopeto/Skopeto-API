from abc import ABC,abstractmethod
from typing import Optional
from app.modules.auth.domain.entity.user import User

class UserRepositoryInterface(ABC):

    @abstractmethod
    def get_by_username_or_email(self, username: str, email: str) -> Optional[User]:
        pass

    @abstractmethod
    def persist(self, user: User) -> User:
        pass