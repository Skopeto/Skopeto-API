import pytest
from unittest.mock import AsyncMock, patch, Mock
from datetime import datetime, timezone, timedelta

from app.modules.auth.application.use_case.user_login_use_case import user_login_use_case
from app.modules.auth.application.request.login_request import LoginRequest
from app.modules.auth.domain.entity.user import User, Roles
from app.core.Exception import SecurityException, ApplicationException


@pytest.mark.asyncio
async def test_user_login_success(mock_user_repository: AsyncMock, sample_user: User):
    """Test successful user login"""
    # Arrange
    request = LoginRequest(
        username="johndoe",
        password="correct_password"
    )

    mock_user_repository.get_by_username.return_value = sample_user

    mock_password_hasher = Mock()
    mock_password_hasher.verify.return_value = True

    with patch('app.modules.auth.application.use_case.user_login_use_case.password_hasher', mock_password_hasher):
        with patch('app.modules.auth.application.use_case.user_login_use_case.create_access_token') as mock_create_token:
            mock_create_token.return_value = "mock_access_token_string"

            # Act
            result = await user_login_use_case(
                request=request,
                user_repository=mock_user_repository
            )

    # Assert
    assert "access_token" in result
    assert result["access_token"] == "mock_access_token_string"
    assert result["token_type"] == "bearer"
    assert result["user_id"] == sample_user.id
    assert "expires_at" in result

    mock_user_repository.get_by_username.assert_called_once_with("johndoe")
    mock_password_hasher.verify.assert_called_once_with(sample_user.hashed_password, "correct_password")
    mock_create_token.assert_called_once()


@pytest.mark.asyncio
async def test_user_login_invalid_username(mock_user_repository: AsyncMock):
    """Test login with invalid username"""
    # Arrange
    request = LoginRequest(
        username="nonexistent",
        password="password"
    )

    mock_user_repository.get_by_username.return_value = None

    # Act & Assert
    with pytest.raises(SecurityException) as exc_info:
        await user_login_use_case(
            request=request,
            user_repository=mock_user_repository
        )

    assert "Invalid username credentials" in str(exc_info.value)
    mock_user_repository.get_by_username.assert_called_once_with("nonexistent")


@pytest.mark.asyncio
async def test_user_login_invalid_password(mock_user_repository: AsyncMock, sample_user: User):
    """Test login with invalid password"""
    # Arrange
    from argon2.exceptions import VerifyMismatchError

    request = LoginRequest(
        username="johndoe",
        password="wrong_password"
    )

    mock_user_repository.get_by_username.return_value = sample_user

    mock_password_hasher = Mock()
    mock_password_hasher.verify.side_effect = VerifyMismatchError()

    with patch('app.modules.auth.application.use_case.user_login_use_case.password_hasher', mock_password_hasher):
        # Act & Assert
        with pytest.raises(SecurityException) as exc_info:
            await user_login_use_case(
                request=request,
                user_repository=mock_user_repository
            )

        assert "Invalid password credentials" in str(exc_info.value)
        mock_user_repository.get_by_username.assert_called_once_with("johndoe")
        mock_password_hasher.verify.assert_called_once_with(sample_user.hashed_password, "wrong_password")


@pytest.mark.asyncio
async def test_user_login_token_creation_failure(mock_user_repository: AsyncMock, sample_user: User):
    """Test login when token creation fails"""
    # Arrange
    request = LoginRequest(
        username="johndoe",
        password="correct_password"
    )

    mock_user_repository.get_by_username.return_value = sample_user

    mock_password_hasher = Mock()
    mock_password_hasher.verify.return_value = True

    with patch('app.modules.auth.application.use_case.user_login_use_case.password_hasher', mock_password_hasher):
        with patch('app.modules.auth.application.use_case.user_login_use_case.create_access_token') as mock_create_token:
            mock_create_token.return_value = None  # Token creation failed

            # Act & Assert
            with pytest.raises(ApplicationException) as exc_info:
                await user_login_use_case(
                    request=request,
                    user_repository=mock_user_repository
                )

            assert "Access token not created" in str(exc_info.value)


@pytest.mark.asyncio
async def test_user_login_superuser(mock_user_repository: AsyncMock, sample_superuser: User):
    """Test superuser login"""
    # Arrange
    request = LoginRequest(
        username="adminuser",
        password="admin_password"
    )

    mock_user_repository.get_by_username.return_value = sample_superuser

    mock_password_hasher = Mock()
    mock_password_hasher.verify.return_value = True

    with patch('app.modules.auth.application.use_case.user_login_use_case.password_hasher', mock_password_hasher):
        with patch('app.modules.auth.application.use_case.user_login_use_case.create_access_token') as mock_create_token:
            mock_create_token.return_value = "superuser_token"

            # Act
            result = await user_login_use_case(
                request=request,
                user_repository=mock_user_repository
            )

    # Assert
    assert result["access_token"] == "superuser_token"
    assert result["user_id"] == sample_superuser.id
    mock_user_repository.get_by_username.assert_called_once_with("adminuser")


@pytest.mark.asyncio
async def test_user_login_token_expires_in_24_hours(mock_user_repository: AsyncMock, sample_user: User):
    """Test that token expires in 24 hours"""
    # Arrange
    request = LoginRequest(
        username="johndoe",
        password="correct_password"
    )

    mock_user_repository.get_by_username.return_value = sample_user

    mock_password_hasher = Mock()
    mock_password_hasher.verify.return_value = True

    with patch('app.modules.auth.application.use_case.user_login_use_case.password_hasher', mock_password_hasher):
        with patch('app.modules.auth.application.use_case.user_login_use_case.create_access_token') as mock_create_token:
            mock_create_token.return_value = "token_string"

            before = datetime.now(timezone.utc)

            # Act
            result = await user_login_use_case(
                request=request,
                user_repository=mock_user_repository
            )

            after = datetime.now(timezone.utc)

    # Assert
    expires_at = datetime.fromisoformat(result["expires_at"])
    expected_min = before + timedelta(hours=24)
    expected_max = after + timedelta(hours=24)

    assert expected_min <= expires_at <= expected_max

    # Verify create_access_token was called with correct expiry delta
    call_args = mock_create_token.call_args
    assert call_args[1]['expires_delta'] == timedelta(hours=24)
