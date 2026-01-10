import pytest
from unittest.mock import AsyncMock
from datetime import datetime, timezone

from app.modules.notifications.application.use_case.update_notification_subscriber import update_notification_subscriber_use_case
from app.modules.notifications.application.request.update_notification_dubscriber_request import UpdateNotificationSubscriberRequest
from app.modules.notifications.domain.entity.notification_subscriber import NotificationSubscriber, NotificationChannel


@pytest.mark.asyncio
async def test_update_notification_subscriber_success(mock_notification_repository: AsyncMock, sample_notification_subscriber: NotificationSubscriber):
    """Test successful update of notification subscriber"""
    # Arrange
    subscriber_id = 1
    request = UpdateNotificationSubscriberRequest(
        user_name="johnupdated",
        delivery_address_email="john.updated@example.com"
    )

    mock_notification_repository.get_subscriber_by_id.return_value = sample_notification_subscriber

    updated_subscriber = NotificationSubscriber(
        id=1,
        user_id=1,
        user_name="johnupdated",
        first_name="John",
        last_name="Doe",
        delivery_address_email="john.updated@example.com",
        notification_channel=NotificationChannel.EMAIL,
        slack_webhook_url=None,
        subscribed_at=datetime(2025, 12, 26, 12, 0, 0, tzinfo=timezone.utc),
        is_active=True
    )
    mock_notification_repository.update_notification_subscriber.return_value = updated_subscriber

    # Act
    result = await update_notification_subscriber_use_case(
        sunbscriber_id=subscriber_id,
        request=request,
        notification_repository=mock_notification_repository
    )

    # Assert
    assert result.user_name == "johnupdated"
    assert result.delivery_address_email == "john.updated@example.com"
    mock_notification_repository.get_subscriber_by_id.assert_called_once_with(subscriber_id)
    mock_notification_repository.update_notification_subscriber.assert_called_once()


@pytest.mark.asyncio
async def test_update_notification_subscriber_change_channel(mock_notification_repository: AsyncMock, sample_notification_subscriber: NotificationSubscriber):
    """Test updating notification channel"""
    # Arrange
    subscriber_id = 1
    request = UpdateNotificationSubscriberRequest(
        notification_channel="slack",
        slack_webhook_url="https://hooks.slack.com/services/NEW"
    )

    mock_notification_repository.get_subscriber_by_id.return_value = sample_notification_subscriber

    updated_subscriber = NotificationSubscriber(
        id=1,
        user_id=1,
        user_name="johndoe",
        first_name="John",
        last_name="Doe",
        delivery_address_email="john.doe@example.com",
        notification_channel=NotificationChannel.SLACK,
        slack_webhook_url="https://hooks.slack.com/services/NEW",
        subscribed_at=datetime(2025, 12, 26, 12, 0, 0, tzinfo=timezone.utc),
        is_active=True
    )
    mock_notification_repository.update_notification_subscriber.return_value = updated_subscriber

    # Act
    result = await update_notification_subscriber_use_case(
        sunbscriber_id=subscriber_id,
        request=request,
        notification_repository=mock_notification_repository
    )

    # Assert
    assert result.notification_channel == NotificationChannel.SLACK
    assert result.slack_webhook_url == "https://hooks.slack.com/services/NEW"
    mock_notification_repository.update_notification_subscriber.assert_called_once()


@pytest.mark.asyncio
async def test_update_notification_subscriber_deactivate(mock_notification_repository: AsyncMock, sample_notification_subscriber: NotificationSubscriber):
    """Test deactivating a subscriber"""
    # Arrange
    subscriber_id = 1
    request = UpdateNotificationSubscriberRequest(is_active=False)

    mock_notification_repository.get_subscriber_by_id.return_value = sample_notification_subscriber

    updated_subscriber = NotificationSubscriber(
        id=1,
        user_id=1,
        user_name="johndoe",
        first_name="John",
        last_name="Doe",
        delivery_address_email="john.doe@example.com",
        notification_channel=NotificationChannel.EMAIL,
        slack_webhook_url=None,
        subscribed_at=datetime(2025, 12, 26, 12, 0, 0, tzinfo=timezone.utc),
        is_active=False
    )
    mock_notification_repository.update_notification_subscriber.return_value = updated_subscriber

    # Act
    result = await update_notification_subscriber_use_case(
        sunbscriber_id=subscriber_id,
        request=request,
        notification_repository=mock_notification_repository
    )

    # Assert
    assert result.is_active is False
    mock_notification_repository.update_notification_subscriber.assert_called_once()


@pytest.mark.asyncio
async def test_update_notification_subscriber_not_found(mock_notification_repository: AsyncMock):
    """Test updating non-existent subscriber"""
    # Arrange
    subscriber_id = 999
    request = UpdateNotificationSubscriberRequest(user_name="newname")

    mock_notification_repository.get_subscriber_by_id.return_value = None

    # Act & Assert
    with pytest.raises(ValueError) as exc_info:
        await update_notification_subscriber_use_case(
            sunbscriber_id=subscriber_id,
            request=request,
            notification_repository=mock_notification_repository
        )

    assert "Notification subscriber with id 999 not found" in str(exc_info.value)
    mock_notification_repository.get_subscriber_by_id.assert_called_once_with(subscriber_id)
    mock_notification_repository.update_notification_subscriber.assert_not_called()
