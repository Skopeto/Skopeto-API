import pytest
from unittest.mock import AsyncMock
from datetime import datetime, timezone

from app.modules.notifications.domain.repository.notification_repository_interface import NotificationRepositoryInterface
from app.modules.notifications.domain.entity.notification_subscriber import NotificationSubscriber, NotificationChannel
from app.modules.notifications.domain.entity.notification import Notification


@pytest.fixture
def mock_notification_repository() -> AsyncMock:
    """Mock NotificationRepositoryInterface with AsyncMock for async methods"""
    return AsyncMock(spec=NotificationRepositoryInterface)


@pytest.fixture
def mock_notification_service() -> AsyncMock:
    """Mock NotificationServiceInterface - using AsyncMock without spec to avoid import issues"""
    return AsyncMock()


@pytest.fixture
def sample_notification_subscriber() -> NotificationSubscriber:
    """Sample NotificationSubscriber entity for testing"""
    return NotificationSubscriber(
        id=1,
        user_id=1,
        user_name="johndoe",
        first_name="John",
        last_name="Doe",
        delivery_address_email="john.doe@example.com",
        notification_channel=NotificationChannel.EMAIL,
        slack_webhook_url=None,
        subscribed_at=datetime(2025, 12, 26, 12, 0, 0, tzinfo=timezone.utc),
        is_active=True
    )


@pytest.fixture
def sample_slack_subscriber() -> NotificationSubscriber:
    """Sample Slack NotificationSubscriber entity for testing"""
    return NotificationSubscriber(
        id=2,
        user_id=2,
        user_name="slackuser",
        first_name="Slack",
        last_name="User",
        delivery_address_email=None,
        notification_channel=NotificationChannel.SLACK,
        slack_webhook_url="https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXX",
        subscribed_at=datetime(2025, 12, 26, 12, 0, 0, tzinfo=timezone.utc),
        is_active=True
    )


@pytest.fixture
def sample_notification() -> Notification:
    """Sample Notification entity for testing"""
    return Notification(
        id=1,
        user_id=1,
        title="Server Alert",
        message="Server is down",
        created_at=datetime(2025, 12, 26, 12, 0, 0, tzinfo=timezone.utc),
        is_read=False
    )
