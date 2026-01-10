import pytest
from unittest.mock import AsyncMock
from datetime import datetime, timezone

from app.modules.notifications.application.use_case.get_subscribers import get_subscribers_use_case
from app.modules.notifications.domain.entity.notification_subscriber import NotificationSubscriber, NotificationChannel


@pytest.mark.asyncio
async def test_get_subscribers_success(mock_notification_repository: AsyncMock, sample_notification_subscriber: NotificationSubscriber, sample_slack_subscriber: NotificationSubscriber):
    """Test successful retrieval of subscribers"""
    # Arrange
    mock_notification_repository.get_subscribers.return_value = [sample_notification_subscriber, sample_slack_subscriber]

    # Act
    result = await get_subscribers_use_case(notification_repository=mock_notification_repository)

    # Assert
    assert len(result) == 2
    assert result[0].id == 1
    assert result[0].notification_channel == NotificationChannel.EMAIL
    assert result[1].id == 2
    assert result[1].notification_channel == NotificationChannel.SLACK
    mock_notification_repository.get_subscribers.assert_called_once()


@pytest.mark.asyncio
async def test_get_subscribers_empty_list(mock_notification_repository: AsyncMock):
    """Test when no subscribers exist"""
    # Arrange
    mock_notification_repository.get_subscribers.return_value = []

    # Act
    result = await get_subscribers_use_case(notification_repository=mock_notification_repository)

    # Assert
    assert result == []
    assert len(result) == 0
    mock_notification_repository.get_subscribers.assert_called_once()


@pytest.mark.asyncio
async def test_get_subscribers_includes_inactive(mock_notification_repository: AsyncMock):
    """Test that get_subscribers includes inactive subscribers"""
    # Arrange
    active = NotificationSubscriber(
        id=1,
        user_id=1,
        user_name="active",
        delivery_address_email="active@example.com",
        notification_channel=NotificationChannel.EMAIL,
        subscribed_at=datetime.now(timezone.utc),
        is_active=True
    )

    inactive = NotificationSubscriber(
        id=2,
        user_id=2,
        user_name="inactive",
        delivery_address_email="inactive@example.com",
        notification_channel=NotificationChannel.EMAIL,
        subscribed_at=datetime.now(timezone.utc),
        is_active=False
    )

    mock_notification_repository.get_subscribers.return_value = [active, inactive]

    # Act
    result = await get_subscribers_use_case(notification_repository=mock_notification_repository)

    # Assert
    assert len(result) == 2
    assert result[0].is_active is True
    assert result[1].is_active is False
    mock_notification_repository.get_subscribers.assert_called_once()
