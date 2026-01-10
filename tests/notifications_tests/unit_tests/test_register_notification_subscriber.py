import pytest
from unittest.mock import AsyncMock
from datetime import datetime, timezone

from app.modules.notifications.application.use_case.register_notification_subscriber import register_notification_subscriber_use_case
from app.modules.notifications.application.request.register_notification_subscriber_request import RegisterNotificationSubscriberRequest
from app.modules.notifications.domain.entity.notification_subscriber import NotificationSubscriber, NotificationChannel


@pytest.mark.asyncio
async def test_register_notification_subscriber_email_success(mock_notification_repository: AsyncMock):
    """Test successful registration of email notification subscriber"""
    # Arrange
    request = RegisterNotificationSubscriberRequest(
        user_id=1,
        user_name="johndoe",
        first_name="John",
        last_name="Doe",
        delivery_address_email="john@example.com",
        notification_channel="email"
    )

    expected_subscriber = NotificationSubscriber(
        id=1,
        user_id=1,
        user_name="johndoe",
        first_name="John",
        last_name="Doe",
        delivery_address_email="john@example.com",
        notification_channel=NotificationChannel.EMAIL,
        slack_webhook_url=None,
        subscribed_at=datetime.now(timezone.utc),
        is_active=True
    )

    mock_notification_repository.persist_notification_subscriber.return_value = expected_subscriber

    # Act
    result = await register_notification_subscriber_use_case(
        request=request,
        notification_repository=mock_notification_repository
    )

    # Assert
    assert result.id == 1
    assert result.user_id == 1
    assert result.user_name == "johndoe"
    assert result.delivery_address_email == "john@example.com"
    assert result.notification_channel == NotificationChannel.EMAIL
    assert result.is_active is True
    mock_notification_repository.persist_notification_subscriber.assert_called_once()


@pytest.mark.asyncio
async def test_register_notification_subscriber_slack_success(mock_notification_repository: AsyncMock):
    """Test successful registration of Slack notification subscriber"""
    # Arrange
    request = RegisterNotificationSubscriberRequest(
        user_id=2,
        user_name="slackuser",
        first_name="Slack",
        last_name="User",
        delivery_address_email=None,
        slack_webhook_url="https://hooks.slack.com/services/XXX",
        notification_channel="slack"
    )

    expected_subscriber = NotificationSubscriber(
        id=2,
        user_id=2,
        user_name="slackuser",
        first_name="Slack",
        last_name="User",
        delivery_address_email=None,
        slack_webhook_url="https://hooks.slack.com/services/XXX",
        notification_channel=NotificationChannel.SLACK,
        subscribed_at=datetime.now(timezone.utc),
        is_active=True
    )

    mock_notification_repository.persist_notification_subscriber.return_value = expected_subscriber

    # Act
    result = await register_notification_subscriber_use_case(
        request=request,
        notification_repository=mock_notification_repository
    )

    # Assert
    assert result.id == 2
    assert result.notification_channel == NotificationChannel.SLACK
    assert result.slack_webhook_url == "https://hooks.slack.com/services/XXX"
    assert result.delivery_address_email is None
    mock_notification_repository.persist_notification_subscriber.assert_called_once()


@pytest.mark.asyncio
async def test_register_notification_subscriber_defaults_to_active(mock_notification_repository: AsyncMock):
    """Test that new subscriber defaults to active"""
    # Arrange
    request = RegisterNotificationSubscriberRequest(
        user_id=1,
        user_name="user",
        delivery_address_email="user@example.com",
        notification_channel="email"
    )

    def persist_side_effect(subscriber: NotificationSubscriber) -> NotificationSubscriber:
        subscriber.id = 1
        return subscriber

    mock_notification_repository.persist_notification_subscriber.side_effect = persist_side_effect

    # Act
    result = await register_notification_subscriber_use_case(
        request=request,
        notification_repository=mock_notification_repository
    )

    # Assert
    assert result.is_active is True

    # Verify the subscriber passed to persist has is_active=True
    call_args = mock_notification_repository.persist_notification_subscriber.call_args
    persisted_subscriber = call_args[0][0]
    assert persisted_subscriber.is_active is True
