from app.modules.notifications.domain.entity.notification import Notification
from app.modules.notifications.domain.repository.notification_repository_interface import NotificationRepositoryInterface


async def get_notifications_use_case(user_id: int, notification_repository: NotificationRepositoryInterface) -> list[Notification | None]:
    notifications = await notification_repository.get_notifications_by_user_id(user_id)
    if not notifications:
        return []
    return notifications