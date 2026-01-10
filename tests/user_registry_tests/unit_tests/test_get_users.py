import pytest
from unittest.mock import AsyncMock

from app.modules.auth.application.use_case.get_users import get_users_use_case
from app.modules.auth.domain.entity.user import User, Roles


@pytest.mark.asyncio
async def test_get_users_success(mock_user_repository: AsyncMock, sample_user: User, sample_superuser: User):
    """Test successful retrieval of users"""
    # Arrange
    user3 = User(
        id=3,
        user_name="regularuser",
        first_name="Regular",
        last_name="User",
        email="user@example.com",
        hashed_password="$argon2id$v=19$m=65536,t=3,p=4$hash3",
        roles=[Roles.USER],
        is_active=True,
        is_superuser=False
    )

    mock_user_repository.get_users.return_value = [sample_user, sample_superuser, user3]

    # Act
    result = await get_users_use_case(user_repository=mock_user_repository)

    # Assert
    assert len(result) == 3
    assert result[0].id == 1
    assert result[0].user_name == "johndoe"
    assert result[0].roles == [Roles.ADMIN]
    assert result[1].id == 2
    assert result[1].user_name == "adminuser"
    assert result[1].roles == [Roles.SUPERADMIN]
    assert result[2].id == 3
    assert result[2].user_name == "regularuser"
    assert result[2].roles == [Roles.USER]
    mock_user_repository.get_users.assert_called_once()


@pytest.mark.asyncio
async def test_get_users_empty_list(mock_user_repository: AsyncMock):
    """Test when no users exist"""
    # Arrange
    mock_user_repository.get_users.return_value = []

    # Act
    result = await get_users_use_case(user_repository=mock_user_repository)

    # Assert
    assert result == []
    assert len(result) == 0
    mock_user_repository.get_users.assert_called_once()


@pytest.mark.asyncio
async def test_get_users_returns_none(mock_user_repository: AsyncMock):
    """Test when repository returns None"""
    # Arrange
    mock_user_repository.get_users.return_value = None

    # Act
    result = await get_users_use_case(user_repository=mock_user_repository)

    # Assert
    assert result is None
    mock_user_repository.get_users.assert_called_once()


@pytest.mark.asyncio
async def test_get_users_different_roles(mock_user_repository: AsyncMock):
    """Test retrieval of users with different roles"""
    # Arrange
    users = [
        User(
            id=1,
            user_name="superadmin1",
            first_name="Super",
            last_name="Admin",
            email="super@example.com",
            hashed_password="hash1",
            roles=[Roles.SUPERADMIN],
            is_active=True,
            is_superuser=True
        ),
        User(
            id=2,
            user_name="admin1",
            first_name="Admin",
            last_name="User",
            email="admin@example.com",
            hashed_password="hash2",
            roles=[Roles.ADMIN],
            is_active=True,
            is_superuser=False
        ),
        User(
            id=3,
            user_name="user1",
            first_name="Regular",
            last_name="User",
            email="user@example.com",
            hashed_password="hash3",
            roles=[Roles.USER],
            is_active=True,
            is_superuser=False
        )
    ]

    mock_user_repository.get_users.return_value = users

    # Act
    result = await get_users_use_case(user_repository=mock_user_repository)

    # Assert
    assert len(result) == 3
    assert result[0].roles == [Roles.SUPERADMIN]
    assert result[0].is_superuser is True
    assert result[1].roles == [Roles.ADMIN]
    assert result[1].is_superuser is False
    assert result[2].roles == [Roles.USER]
    assert result[2].is_superuser is False
    mock_user_repository.get_users.assert_called_once()


@pytest.mark.asyncio
async def test_get_users_includes_inactive_users(mock_user_repository: AsyncMock):
    """Test that get_users includes inactive users"""
    # Arrange
    active_user = User(
        id=1,
        user_name="activeuser",
        first_name="Active",
        last_name="User",
        email="active@example.com",
        hashed_password="hash1",
        roles=[Roles.USER],
        is_active=True,
        is_superuser=False
    )

    inactive_user = User(
        id=2,
        user_name="inactiveuser",
        first_name="Inactive",
        last_name="User",
        email="inactive@example.com",
        hashed_password="hash2",
        roles=[Roles.USER],
        is_active=False,
        is_superuser=False
    )

    mock_user_repository.get_users.return_value = [active_user, inactive_user]

    # Act
    result = await get_users_use_case(user_repository=mock_user_repository)

    # Assert
    assert len(result) == 2
    assert result[0].is_active is True
    assert result[1].is_active is False
    mock_user_repository.get_users.assert_called_once()
