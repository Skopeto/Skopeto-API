from typing import Any

from app.modules.notifications.domain.entity.notification_subscriber import (
    NotificationSubscriber,
)
from app.modules.notifications.domain.entity.notification import Notification


def create_notification_query(notification: Notification) -> tuple[str, dict[str, Any]]:
    query = """
        INSERT INTO notifications (
            user_id,
            title,
            message,
            created_at,
            is_read
        )
        VALUES (
            :user_id, :title, :message, :created_at, :is_read
        )
    """
    params = {
        "user_id": notification.user_id,
        "title": notification.title,
        "message": notification.message,
        "created_at": notification.created_at.replace(tzinfo=None) if notification.created_at else None,
        "is_read": notification.is_read,
    }
    return query, params

def get_notification_by_id_query(user_id: int) -> tuple[str, dict[str, Any]]:
    query = """
        SELECT
            id,
            user_id,
            title,
            message,
            created_at,
            is_read
        FROM notifications
        WHERE user_id = :user_id
    """
    params = {"user_id": user_id}
    return query, params

def mark_notification_as_read_query(notification_id: int) -> tuple[str, dict[str, Any]]:
    query = """
        UPDATE notifications
        SET is_read = TRUE
        WHERE id = :notification_id
    """
    params = {"notification_id": notification_id}
    return query, params


def delete_notification_query(notification_id: int) -> tuple[str, dict[str, Any]]:
    query = """
        DELETE FROM notifications
        WHERE id = :notification_id
    """
    params = {"notification_id": notification_id}
    return query, params


def get_active_subscribers_query() -> tuple[str, dict[str, Any]]:
    query = """
        SELECT id, user_id, user_name, first_name, last_name, delivery_address_email, notification_channel, slack_webhook_url, subscribed_at, is_active
        FROM notification_subscribers
        WHERE is_active = TRUE
    """
    params = {}
    return query, params


def get_subscriber_by_id_query(subscriber_id: int) -> tuple[str, dict[str, Any]]:
    query = """
        SELECT id, user_id, user_name, first_name, last_name, delivery_address_email, notification_channel, slack_webhook_url, subscribed_at, is_active
        FROM notification_subscribers
        WHERE id = :subscriber_id
    """
    params = {"subscriber_id": subscriber_id}
    return query, params


def persist_notification_subscriber_query(
    notification_subscriber: NotificationSubscriber,
) -> tuple[str, dict[str, Any]]:
    query = """
                INSERT INTO notification_subscribers (user_id, user_name, first_name, last_name, delivery_address_email, notification_channel, slack_webhook_url, subscribed_at, is_active)
                VALUES (:user_id, :user_name,:first_name, :last_name, :delivery_address_email, :notification_channel, :slack_webhook_url, :subscribed_at, :is_active)
                RETURNING id, user_id, user_name,first_name, last_name, delivery_address_email, notification_channel, slack_webhook_url, subscribed_at, is_active
            """
    params = {
        "user_id": notification_subscriber.user_id,
        "user_name": notification_subscriber.user_name,
        "first_name": notification_subscriber.first_name,
        "last_name": notification_subscriber.last_name,
        "delivery_address_email": notification_subscriber.delivery_address_email,
        "notification_channel": notification_subscriber.notification_channel.value,
        "slack_webhook_url": notification_subscriber.slack_webhook_url,
        "subscribed_at": notification_subscriber.subscribed_at.replace(tzinfo=None) if notification_subscriber.subscribed_at else None,
        "is_active": notification_subscriber.is_active,
    }
    return query, params


def update_notification_subscriber_query(
    notification_subscriber: NotificationSubscriber,
) -> tuple[str, dict[str, Any]]:
    query = """
                UPDATE notification_subscribers
                SET user_id = :user_id,
                    user_name = :user_name,
                    delivery_address_email = :delivery_address_email,
                    notification_channel = :notification_channel,
                    slack_webhook_url = :slack_webhook_url,
                    subscribed_at = :subscribed_at,
                    is_active = :is_active
                WHERE id = :id
                RETURNING id, user_id, user_name, delivery_address_email, notification_channel, slack_webhook_url, subscribed_at, is_active
            """
    params = {
        "id": notification_subscriber.id,
        "user_id": notification_subscriber.user_id,
        "user_name": notification_subscriber.user_name,
        "delivery_address_email": notification_subscriber.delivery_address_email,
        "notification_channel": notification_subscriber.notification_channel.value,
        "slack_webhook_url": notification_subscriber.slack_webhook_url,
        "subscribed_at": notification_subscriber.subscribed_at.replace(tzinfo=None) if notification_subscriber.subscribed_at else None,
        "is_active": notification_subscriber.is_active,
    }
    return query, params

def delete_notification_subscriber_query(
    subscriber_id: int,
) -> tuple[str, dict[str, Any]]:
    query = """
                DELETE FROM notification_subscribers
                WHERE id = :subscriber_id
            """
    params = {"subscriber_id": subscriber_id}
    return query, params

def get_subscribers_query() -> tuple[str, dict[str, Any]]:
    query = """
        SELECT id, user_id, user_name, first_name, last_name, delivery_address_email, notification_channel, slack_webhook_url, subscribed_at, is_active
        FROM notification_subscribers
    """
    params = {}
    return query, params

