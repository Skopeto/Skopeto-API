from datetime import datetime, timezone
from app.modules.notifications.application.request.register_notification_subscriber_request import RegisterNotificationSubscriberRequest
from app.modules.notifications.domain.entity.notification_subscriber import NotificationChannel, NotificationSubscriber
from app.modules.notifications.domain.repository.notification_repository_interface import NotificationRepositoryInterface


async def register_notification_subscriber_use_case(
    request: RegisterNotificationSubscriberRequest,
    notification_repository: NotificationRepositoryInterface
) -> NotificationSubscriber:

    notification_subscriber = NotificationSubscriber(
        user_id=request.user_id,
        user_name=request.user_name,
        first_name=request.first_name,
        last_name=request.last_name,
        delivery_address_email=request.delivery_address_email,
        slack_webhook_url=request.slack_webhook_url,
        notification_channel=NotificationChannel(request.notification_channel),
        subscribed_at=datetime.now(timezone.utc),
        is_active=True
    )
    saved_subscriber = await notification_repository.persist_notification_subscriber(notification_subscriber)
    return saved_subscriber