from app.core.Exception import AuthorizationException
from app.modules.auth.domain.entity.user import Roles, User

async def check_if_user_superadmin(current_user: User) -> None:
    if current_user.roles != Roles.SUPERADMIN:
        raise AuthorizationException()