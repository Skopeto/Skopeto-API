from typing import Any
import logging
import datetime
from app.core.Exception import RepositoryException
from app.core.base_repository import SqlBaseRepository
from app.core.sql_query import SqlQuery
from app.modules.notifications.domain.entity.notification import Notification
from app.modules.notifications.domain.entity.notification_subscriber import NotificationSubscriber, NotificationChannel
from app.modules.notifications.domain.repository.notification_repository_interface import NotificationRepositoryInterface
from app.modules.notifications.infrastructure.sql_query.notification_query import create_notification_query, delete_notification_query, delete_notification_subscriber_query, get_active_subscribers_query, get_notification_by_id_query, get_subscriber_by_id_query, get_subscribers_query, mark_notification_as_read_query, persist_notification_subscriber_query, update_notification_subscriber_query


logger = logging.getLogger(__name__)

def notification_from_db(row: dict[str, Any] | None) -> Notification | None:
    if not row:
        return None
    
        # Add UTC timezone to naive datetime from database
    created_at = row['created_at']
    if created_at and created_at.tzinfo is None:
        created_at = created_at.replace(tzinfo=datetime.timezone.utc)

    notification_attrs = {
        'id': row['id'],
        'user_id': row['user_id'],
        'title': row['title'],
        'message': row['message'],
        'created_at': row['created_at'],
        'is_read': row['is_read'],
    }
    
    return Notification.model_construct(**notification_attrs)

def notification_subsciber_from_db(row: dict[str, Any] | None) -> NotificationSubscriber | None:
    if not row:
        return None

    subscribed_at = row['subscribed_at']
    if subscribed_at and subscribed_at.tzinfo is None:
        subscribed_at = subscribed_at.replace(tzinfo=datetime.timezone.utc)

    notification_subsciber_attrs = {
        'id': row['id'],
        'user_id': row['user_id'],
        'user_name': row['user_name'],
        'first_name': row['first_name'],
        'last_name': row['last_name'],
        'delivery_address_email': row['delivery_address_email'],
        'notification_channel': NotificationChannel(row['notification_channel']),
        'slack_webhook_url': row['slack_webhook_url'],
        'subscribed_at': row['subscribed_at'],
        'is_active': row['is_active'],
    }

    return NotificationSubscriber.model_construct(**notification_subsciber_attrs)

class SqlNotificationRepository(NotificationRepositoryInterface, SqlBaseRepository):
    async def create_notification(self, notification: Notification) -> None:
        try:
            query,params = create_notification_query(notification)
            sql_query = SqlQuery(self.session, query, params)
            await sql_query.persist()
        except Exception as e:
            logger.error(f"Error creating notification: {e}")
            raise RepositoryException("Failed to create notification") from e
        
    async def get_notifications_by_user_id(self, user_id: int) -> list[Notification | None]:
        try:
            query, params = get_notification_by_id_query(user_id)
            sql_query = SqlQuery(self.session, query, params)
            return await sql_query.fetch_all(transformer=notification_from_db)
        except Exception as e:
            logger.error(f"Error fetching notification by id {user_id}: {e}")
            raise RepositoryException("Failed to fetch notification") from e
        
    async def mark_notification_as_read(self, notification_id: int) -> None:
        try:
            query, params = mark_notification_as_read_query(notification_id)
            sql_query = SqlQuery(self.session, query, params)
            await sql_query.persist()
        except Exception as e:
            logger.error(f"Error marking notification {notification_id} as read: {e}")
            raise RepositoryException("Failed to mark notification as read") from e
        
    async def delete_notification(self, notification_id: int) -> None:
        try:
            query, params = delete_notification_query(notification_id)
            sql_query = SqlQuery(self.session, query, params)
            await sql_query.delete()
        except Exception as e:
            logger.error(f"Error deleting notification {notification_id}: {e}")
            raise RepositoryException("Failed to delete notification") from e

    async def get_active_subscribers(self) -> list[NotificationSubscriber | None]:
       try:
            query ,params = get_active_subscribers_query()
            sql_query = SqlQuery(self.session, query, params)
            rows = await sql_query.fetch_all(transformer=notification_subsciber_from_db)
            return rows
       except Exception as e:
            logger.error(f"Error fetching active notification subscribers: {e}")
            raise RepositoryException("Failed to fetch active notification subscribers") from e
        
    async def persist_notification_subscriber(self, notification_subscriber: NotificationSubscriber) -> NotificationSubscriber | None:
        try:
            query, params = persist_notification_subscriber_query(notification_subscriber)
            sql_query = SqlQuery(self.session, query, params)
            await sql_query.persist()
            return notification_subscriber
        except Exception as e:
            logger.error(f"Error persisting notification subscriber: {e}")
            raise RepositoryException("Failed to persist notification subscriber") from e
        
    async def update_notification_subscriber(self, notification_subscriber: NotificationSubscriber) -> NotificationSubscriber | None:
        try:
            query, params = update_notification_subscriber_query(notification_subscriber)
            sql_query = SqlQuery(self.session, query, params)
            await sql_query.persist()
            return notification_subscriber
        except Exception as e:
            logger.error(f"Error updating notification subscriber {notification_subscriber.id}: {e}")
            raise RepositoryException("Failed to update notification subscriber") from e
        
    async def delete_notification_subscriber(self, subscriber_id: int) -> None:
        try:
            query, params = delete_notification_subscriber_query(subscriber_id)
            sql_query = SqlQuery(self.session, query, params)
            await sql_query.delete()
        except Exception as e:
            logger.error(f"Error deleting notification subscriber {subscriber_id}: {e}")
            raise RepositoryException("Failed to delete notification subscriber") from e
        
    async def get_subscriber_by_id(self, subscriber_id: int) -> NotificationSubscriber | None:
        try:
            query, params = get_subscriber_by_id_query(subscriber_id)
            sql_query = SqlQuery(self.session, query, params)
            return await sql_query.fetch_one(transformer=notification_subsciber_from_db)
        except Exception as e:
            logger.error(f"Error fetching notification subscriber by id {subscriber_id}: {e}")
            raise RepositoryException("Failed to fetch notification subscriber") from e
        
    async def get_subscribers(self) -> list[NotificationSubscriber | None]:
        try:
            query ,params = get_subscribers_query()
            sql_query = SqlQuery(self.session, query, params)
            rows = await sql_query.fetch_all(transformer=notification_subsciber_from_db)
            return rows
        except Exception as e:
            logger.error(f"Error fetching notification subscribers: {e}")
            raise RepositoryException("Failed to fetch notification subscribers") from e
        
    