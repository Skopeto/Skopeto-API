from app.modules.notifications.domain.repository.notification_repository_interface import NotificationRepositoryInterface

async def delete_notification_use_case(
    notification_id: int,
    notification_repository: NotificationRepositoryInterface,
) -> None:
    await notification_repository.delete_notification(notification_id)