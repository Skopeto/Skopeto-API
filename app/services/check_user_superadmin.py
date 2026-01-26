from app.core.Exception import AuthorizationException
from app.modules.auth.domain.entity.user import Roles, User

async def check_if_user_superadmin(current_user: User) -> None:
    if Roles.SUPERADMIN not in current_user.roles:
        raise AuthorizationException()