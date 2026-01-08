from datetime import datetime, timezone
from app.modules.notifications.application.service.notification_service import NotificationServiceInterface
from app.modules.notifications.domain.entity.notification import Notification
from app.modules.notifications.domain.repository.notification_repository_interface import NotificationRepositoryInterface

async def create_notification_and_notify_subscriber(
    message: str,
    title: str,
    notification_repository: NotificationRepositoryInterface,
    notification_service: NotificationServiceInterface
) -> None:
    
    notification_subscribers = await notification_repository.get_active_subscribers()
    if not notification_subscribers:
        return
    for subscriber in notification_subscribers:
        await notification_service.send_notification_to_subscribers(subscriber, title, message)

        notification = Notification(
            user_id=subscriber.user_id,
            title=title,
            message=message,
            created_at=datetime.now(timezone.utc),
            is_read=False
        )
        await notification_repository.create_notification(notification)

    
