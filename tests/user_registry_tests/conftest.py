import pytest
from unittest.mock import AsyncMock

from app.modules.auth.domain.repository.user_repository import UserRepositoryInterface
from app.modules.auth.domain.entity.user import User, Roles


@pytest.fixture
def mock_user_repository() -> AsyncMock:
    """Mock UserRepositoryInterface with AsyncMock for async methods"""
    return AsyncMock(spec=UserRepositoryInterface)


@pytest.fixture
def sample_user() -> User:
    """Sample User entity for testing"""
    return User(
        id=1,
        user_name="johndoe",
        first_name="John",
        last_name="Doe",
        email="john.doe@example.com",
        hashed_password="$argon2id$v=19$m=65536,t=3,p=4$somehash",
        roles=[Roles.ADMIN],
        is_active=True,
        is_superuser=False
    )


@pytest.fixture
def sample_superuser() -> User:
    """Sample superuser entity for testing"""
    return User(
        id=2,
        user_name="adminuser",
        first_name="Admin",
        last_name="User",
        email="admin@example.com",
        hashed_password="$argon2id$v=19$m=65536,t=3,p=4$adminhash",
        roles=[Roles.SUPERADMIN],
        is_active=True,
        is_superuser=True
    )
