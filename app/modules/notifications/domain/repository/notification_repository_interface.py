from abc import ABC, abstractmethod
from app.modules.notifications.domain.entity.notification import Notification
from app.modules.notifications.domain.entity.notification_subscriber import NotificationSubscriber

class NotificationRepositoryInterface(ABC):
    @abstractmethod
    async def create_notification(self, notification: Notification) -> Notification:
        pass

    @abstractmethod
    async def get_notification_by_id(self, notification_id: int) -> Notification | None:
        pass

    @abstractmethod
    async def mark_notification_as_read(self, notification_id: int) -> None:
        pass

    @abstractmethod
    async def delete_notification(self, notification_id: int) -> None:
        pass

    @abstractmethod
    async def get_active_subscribers(self) -> list[NotificationSubscriber]:
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

    @abstractmethod
    async def get_subscriber_by_id(self, subscriber_id: int) -> NotificationSubscriber | None:
        pass

    @abstractmethod
    async def get_subscribers(self) -> list[NotificationSubscriber | None]:
        pass

