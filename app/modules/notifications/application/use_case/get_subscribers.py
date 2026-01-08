from app.modules.notifications.domain.entity.notification_subscriber import NotificationSubscriber
from app.modules.notifications.domain.repository.notification_repository_interface import NotificationRepositoryInterface

async def get_subscribers_use_case(
    notification_repository: NotificationRepositoryInterface
) -> list[NotificationSubscriber | None]:
    subscribers = await notification_repository.get_subscribers()
    return subscribers