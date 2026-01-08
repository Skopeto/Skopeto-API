from app.core.db_session import SessionDep
from app.modules.notifications.domain.repository.notification_repository_interface import (
    NotificationRepositoryInterface,
)
from app.modules.notifications.infrastructure.sql_repository.notification_repository import (
    SqlNotificationRepository,
)

def get_notification_repository(session: SessionDep) -> NotificationRepositoryInterface:
    return SqlNotificationRepository(session)
