from app.modules.notifications.application.request.update_notification_dubscriber_request import (
    UpdateNotificationSubscriberRequest,
)
from app.modules.notifications.domain.entity.notification_subscriber import (
    NotificationChannel,
    NotificationSubscriber,
)
from app.modules.notifications.domain.repository.notification_repository_interface import (
    NotificationRepositoryInterface,
)

async def update_notification_subscriber_use_case(
    sunbscriber_id: int,
    request: UpdateNotificationSubscriberRequest,
    notification_repository: NotificationRepositoryInterface,
) -> NotificationSubscriber:
    existing_subscriber = await notification_repository.get_subscriber_by_id(
        sunbscriber_id
    )

    if existing_subscriber is None:
        raise ValueError(
            f"Notification subscriber with id {sunbscriber_id} not found"
        )

    updates = {}
    if request.user_name is not None:
        updates["user_name"] = request.user_name
    if request.delivery_address_email is not None:
        updates["delivery_address_email"] = request.delivery_address_email
    if request.slack_webhook_url is not None:
        updates["slack_webhook_url"] = request.slack_webhook_url
    if request.notification_channel is not None:
        updates["notification_channel"] = NotificationChannel(
            request.notification_channel
        )
    if request.is_active is not None:
        updates["is_active"] = request.is_active

    updated_subscriber = existing_subscriber.model_copy(update=updates)
    return await notification_repository.update_notification_subscriber(
        updated_subscriber
    )
