from app.modules.notifications.domain.repository.notification_repository_interface import NotificationRepositoryInterface

async def mark_notification_as_read_use_case(
    notification_id: int,
    notification_repository: NotificationRepositoryInterface
) -> None:
    await notification_repository.mark_notification_as_read(notification_id)