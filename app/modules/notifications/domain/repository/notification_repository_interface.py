from abc import ABC, abstractmethod
from app.modules.notifications.domain.entity.notification import Notification
from app.modules.notifications.domain.entity.notification_subscriber import NotificationSubscriber

class NotificationRepositoryInterface(ABC):
    @abstractmethod
    async def get_active_subscribers(self) -> list[NotificationSubscriber]:
        pass

    @abstractmethod
    async def create_notification(self, notification: Notification) -> Notification:
        pass

    @abstractmethod
    async def persist_notification_subscriber(self, notification_subscriber: NotificationSubscriber) -> NotificationSubscriber:
        pass

    @abstractmethod
    async def update_notification_subscriber(self, notification_subscriber: NotificationSubscriber) -> NotificationSubscriber:
        pass

    @abstractmethod
    async def delete_notification_subscriber(self, subscriber_id: int) -> None:
        pass    