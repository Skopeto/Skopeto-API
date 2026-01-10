import pytest
from unittest.mock import AsyncMock
from datetime import datetime, timezone

from app.modules.notifications.application.use_case.delete_notification import delete_notification_use_case
from app.modules.notifications.application.use_case.mark_notification_as_read import mark_notification_as_read_use_case
from app.modules.notifications.application.use_case.create_notification_and_notify_subscriber import create_notification_and_notify_subscriber
from app.modules.notifications.domain.entity.notification_subscriber import NotificationSubscriber, NotificationChannel
from app.modules.notifications.domain.entity.notification import Notification


@pytest.mark.asyncio
async def test_delete_notification_success(mock_notification_repository: AsyncMock):
    """Test successful deletion of notification"""
    # Arrange
    notification_id = 1
    mock_notification_repository.delete_notification.return_value = None

    # Act
    result = await delete_notification_use_case(
        notification_id=notification_id,
        notification_repository=mock_notification_repository
    )

    # Assert
    assert result is None
    mock_notification_repository.delete_notification.assert_called_once_with(notification_id)


@pytest.mark.asyncio
async def test_mark_notification_as_read_success(mock_notification_repository: AsyncMock):
    """Test successfully marking notification as read"""
    # Arrange
    notification_id = 1
    mock_notification_repository.mark_notification_as_read.return_value = None

    # Act
    result = await mark_notification_as_read_use_case(
        notification_id=notification_id,
        notification_repository=mock_notification_repository
    )

    # Assert
    assert result is None
    mock_notification_repository.mark_notification_as_read.assert_called_once_with(notification_id)


@pytest.mark.asyncio
async def test_create_notification_and_notify_subscriber_success(
    mock_notification_repository: AsyncMock,
    mock_notification_service: AsyncMock,
    sample_notification_subscriber: NotificationSubscriber
):
    """Test creating notification and notifying subscribers"""
    # Arrange
    title = "Server Alert"
    message = "Server is down"

    mock_notification_repository.get_active_subscribers.return_value = [sample_notification_subscriber]
    mock_notification_service.send_notification_to_subscribers.return_value = None
    mock_notification_repository.create_notification.return_value = None

    # Act
    result = await create_notification_and_notify_subscriber(
        message=message,
        title=title,
        notification_repository=mock_notification_repository,
        notification_service=mock_notification_service
    )

    # Assert
    assert result is None
    mock_notification_repository.get_active_subscribers.assert_called_once()
    mock_notification_service.send_notification_to_subscribers.assert_called_once()
    mock_notification_repository.create_notification.assert_called_once()

    # Verify notification was sent to the subscriber
    call_args = mock_notification_service.send_notification_to_subscribers.call_args
    assert call_args[0][0] == sample_notification_subscriber
    assert call_args[0][1] == title
    assert call_args[0][2] == message


@pytest.mark.asyncio
async def test_create_notification_no_active_subscribers(
    mock_notification_repository: AsyncMock,
    mock_notification_service: AsyncMock
):
    """Test creating notification when no active subscribers exist"""
    # Arrange
    title = "Server Alert"
    message = "Server is down"

    mock_notification_repository.get_active_subscribers.return_value = []

    # Act
    result = await create_notification_and_notify_subscriber(
        message=message,
        title=title,
        notification_repository=mock_notification_repository,
        notification_service=mock_notification_service
    )

    # Assert
    assert result is None
    mock_notification_repository.get_active_subscribers.assert_called_once()
    mock_notification_service.send_notification_to_subscribers.assert_not_called()
    mock_notification_repository.create_notification.assert_not_called()


@pytest.mark.asyncio
async def test_create_notification_multiple_subscribers(
    mock_notification_repository: AsyncMock,
    mock_notification_service: AsyncMock,
    sample_notification_subscriber: NotificationSubscriber,
    sample_slack_subscriber: NotificationSubscriber
):
    """Test creating notification for multiple subscribers"""
    # Arrange
    title = "Server Alert"
    message = "Server is down"

    mock_notification_repository.get_active_subscribers.return_value = [
        sample_notification_subscriber,
        sample_slack_subscriber
    ]
    mock_notification_service.send_notification_to_subscribers.return_value = None
    mock_notification_repository.create_notification.return_value = None

    # Act
    result = await create_notification_and_notify_subscriber(
        message=message,
        title=title,
        notification_repository=mock_notification_repository,
        notification_service=mock_notification_service
    )

    # Assert
    assert result is None
    assert mock_notification_service.send_notification_to_subscribers.call_count == 2
    assert mock_notification_repository.create_notification.call_count == 2
    mock_notification_repository.get_active_subscribers.assert_called_once()
