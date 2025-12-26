import pytest
from unittest.mock import Mock
from app.modules.auth.application.request.register_user_request import RegisterUserRequest, UserType
from app.modules.auth.application.use_case.register_user_use_case import register_user_use_case
from app.modules.auth.domain.entity.user import Roles, User
from app.modules.auth.domain.repository.user_repository import UserRepositoryInterface

# -------------------- Fixtures --------------------

@pytest.fixture
def mock_user() -> User:
    return User(
        id=1,
        user_name="johndoe",
        first_name="John",
        last_name="Doe",
        email="johnlesis91@gmail.com",
        hashed_password="$argon2id$v=19$m=65536,t=3,p=4$somehash",
        roles=[Roles.ADMIN]
    )

@pytest.fixture(scope="function")
def mock_user_repository(): 
    repo = Mock(spec=UserRepositoryInterface)
    # Mock get_by_username_or_email to return None (user does not exist)
    repo.get_by_username_or_email.return_value = None
    return repo

@pytest.fixture(scope="function")
def valid_register_user_request() -> RegisterUserRequest:
    return RegisterUserRequest(
        first_name="John",
        last_name="Doe",
        user_name="johndoe",
        email="johnlesis91@gmail.com",
        password="SecurePass123!",
        user_type=UserType.ADMIN
    )

# -------------------- Test Case --------------------

@pytest.mark.asyncio
async def test_register_user_success(
    valid_register_user_request: RegisterUserRequest,
    mock_user_repository: Mock,
    mock_user: User
):
    def persist_side_effect(user: User) -> User:
        user.id = mock_user.id
        return user

    mock_user_repository.persist_user.side_effect = persist_side_effect
    
    registered_user: User = await register_user_use_case(
        request=valid_register_user_request,
        user_repository=mock_user_repository
    )

    assert registered_user.user_name == valid_register_user_request.user_name
    assert registered_user.email == valid_register_user_request.email
    assert registered_user.first_name == valid_register_user_request.first_name
    assert registered_user.last_name == valid_register_user_request.last_name
    assert registered_user.roles == [Roles.ADMIN]
    assert len(registered_user.roles) == 1
    assert registered_user.roles[0].value == valid_register_user_request.user_type.value
    assert registered_user.id == mock_user.id
    assert registered_user.hashed_password != valid_register_user_request.password
    
    mock_user_repository.persist_user.assert_called_once()
