from app.core.Exception import ApplicationException
from app.modules.notifications.domain.entity.notification import Notification
from app.modules.notifications.domain.repository.notification_repository_interface import NotificationRepositoryInterface


async def get_subscriber_notifications_use_case(user_id: int, notification_repository: NotificationRepositoryInterface) -> list[Notification | None]:
    subscribed_user = await notification_repository.get_subscriber_by_id(user_id)
    if not subscribed_user:
        raise ApplicationException("user with id {user_id} not subscibed to receive notifications")
    
    notifications = await notification_repository.get_notification_by_user_id(user_id)
    
    if not notifications:
        return []
    
    return notifications