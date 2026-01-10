import pytest
from unittest.mock import AsyncMock

from app.modules.auth.application.use_case.get_user import get_user_use_case
from app.modules.auth.domain.entity.user import User, Roles


@pytest.mark.asyncio
async def test_get_user_success(mock_user_repository: AsyncMock, sample_user: User):
    """Test successful retrieval of a user by ID"""
    # Arrange
    user_id = 1
    mock_user_repository.get_user.return_value = sample_user

    # Act
    result = await get_user_use_case(
        user_id=user_id,
        user_repository=mock_user_repository
    )

    # Assert
    assert result.id == 1
    assert result.user_name == "johndoe"
    assert result.first_name == "John"
    assert result.last_name == "Doe"
    assert result.email == "john.doe@example.com"
    assert result.roles == [Roles.ADMIN]
    assert result.is_active is True
    mock_user_repository.get_user.assert_called_once_with(user_id)


@pytest.mark.asyncio
async def test_get_user_not_found(mock_user_repository: AsyncMock):
    """Test retrieval when user doesn't exist"""
    # Arrange
    user_id = 999
    mock_user_repository.get_user.return_value = None

    # Act
    result = await get_user_use_case(
        user_id=user_id,
        user_repository=mock_user_repository
    )

    # Assert
    assert result is None
    mock_user_repository.get_user.assert_called_once_with(user_id)


@pytest.mark.asyncio
async def test_get_user_superuser(mock_user_repository: AsyncMock, sample_superuser: User):
    """Test retrieval of a superuser"""
    # Arrange
    user_id = 2
    mock_user_repository.get_user.return_value = sample_superuser

    # Act
    result = await get_user_use_case(
        user_id=user_id,
        user_repository=mock_user_repository
    )

    # Assert
    assert result.id == 2
    assert result.user_name == "adminuser"
    assert result.roles == [Roles.SUPERADMIN]
    assert result.is_superuser is True
    mock_user_repository.get_user.assert_called_once_with(user_id)


@pytest.mark.asyncio
async def test_get_user_inactive(mock_user_repository: AsyncMock):
    """Test retrieval of an inactive user"""
    # Arrange
    inactive_user = User(
        id=3,
        user_name="inactiveuser",
        first_name="Inactive",
        last_name="User",
        email="inactive@example.com",
        hashed_password="hash",
        roles=[Roles.USER],
        is_active=False,
        is_superuser=False
    )

    user_id = 3
    mock_user_repository.get_user.return_value = inactive_user

    # Act
    result = await get_user_use_case(
        user_id=user_id,
        user_repository=mock_user_repository
    )

    # Assert
    assert result.id == 3
    assert result.is_active is False
    mock_user_repository.get_user.assert_called_once_with(user_id)


@pytest.mark.asyncio
async def test_get_user_with_different_ids(mock_user_repository: AsyncMock):
    """Test retrieval with various user IDs"""
    # Test with different IDs
    test_ids = [1, 10, 100, 999]

    for test_id in test_ids:
        mock_user_repository.reset_mock()

        test_user = User(
            id=test_id,
            user_name=f"user{test_id}",
            first_name="Test",
            last_name="User",
            email=f"user{test_id}@example.com",
            hashed_password="hash",
            roles=[Roles.USER],
            is_active=True,
            is_superuser=False
        )

        mock_user_repository.get_user.return_value = test_user

        # Act
        result = await get_user_use_case(
            user_id=test_id,
            user_repository=mock_user_repository
        )

        # Assert
        assert result.id == test_id
        assert result.user_name == f"user{test_id}"
        mock_user_repository.get_user.assert_called_once_with(test_id)
