from app.core.Exception import ApplicationException
from app.modules.notifications.domain.repository.notification_repository_interface import NotificationRepositoryInterface

async def delete_notification_subscriber_use_case(
    subscriber_id: int,
    notification_repository: NotificationRepositoryInterface,
) -> None:
    existing_subscriber = await notification_repository.get_subscriber_by_id(
        subscriber_id
    )
    if existing_subscriber is None:
        raise ApplicationException(
            f"Notification subscriber with id {subscriber_id} not found"
        )
    
    await notification_repository.delete_notification_subscriber(subscriber_id)