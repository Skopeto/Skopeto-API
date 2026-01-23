from datetime import datetime, timezone
import logging
from app.modules.auth.domain.repository.user_repository import UserRepositoryInterface
from app.modules.notifications.application.service.notification_service import NotificationServiceInterface
from app.modules.notifications.domain.entity.notification import Notification
from app.modules.notifications.domain.repository.notification_repository_interface import NotificationRepositoryInterface

logger = logging.getLogger(__name__)

async def create_notification_for_all_users(
    message: str,
    title: str,
    user_repository : UserRepositoryInterface,
    notification_repository: NotificationRepositoryInterface,
    notification_service: NotificationServiceInterface
) -> None:
    all_users = await user_repository.get_users()
    active_subscribers = await notification_repository.get_active_subscribers()
    
    subscriber_ids = {sub.user_id for sub in active_subscribers}
    if all_users:
        for user in all_users:
            notification = Notification(
                user_id=user.id,
                title=title,
                message=message,
                created_at=datetime.now(timezone.utc),
                is_read=False
            )
        
            await notification_repository.create_notification(notification)
            
            if user.id in subscriber_ids:
                try:
                    subscriber = next(sub for sub in active_subscribers if sub.user_id == user.id)
                    await notification_service.send_notification_to_subscribers(subscriber, title, message)
                except Exception as e:
                    logger.error(f"Failed to send email to user {user.id}: {e}")