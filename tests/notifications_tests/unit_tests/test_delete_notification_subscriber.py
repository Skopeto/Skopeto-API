import pytest
from unittest.mock import AsyncMock

from app.modules.notifications.application.use_case.delete_notification_subscriber import delete_notification_subscriber_use_case
from app.modules.notifications.domain.entity.notification_subscriber import NotificationSubscriber
from app.core.Exception import ApplicationException


@pytest.mark.asyncio
async def test_delete_notification_subscriber_success(mock_notification_repository: AsyncMock, sample_notification_subscriber: NotificationSubscriber):
    """Test successful deletion of notification subscriber"""
    # Arrange
    subscriber_id = 1
    mock_notification_repository.get_subscriber_by_id.return_value = sample_notification_subscriber
    mock_notification_repository.delete_notification_subscriber.return_value = None

    # Act
    result = await delete_notification_subscriber_use_case(
        subscriber_id=subscriber_id,
        notification_repository=mock_notification_repository
    )

    # Assert
    assert result is None
    mock_notification_repository.get_subscriber_by_id.assert_called_once_with(subscriber_id)
    mock_notification_repository.delete_notification_subscriber.assert_called_once_with(subscriber_id)


@pytest.mark.asyncio
async def test_delete_notification_subscriber_not_found(mock_notification_repository: AsyncMock):
    """Test deleting non-existent subscriber"""
    # Arrange
    subscriber_id = 999
    mock_notification_repository.get_subscriber_by_id.return_value = None

    # Act & Assert
    with pytest.raises(ApplicationException) as exc_info:
        await delete_notification_subscriber_use_case(
            subscriber_id=subscriber_id,
            notification_repository=mock_notification_repository
        )

    assert "Notification subscriber with id 999 not found" in str(exc_info.value)
    mock_notification_repository.get_subscriber_by_id.assert_called_once_with(subscriber_id)
    mock_notification_repository.delete_notification_subscriber.assert_not_called()
