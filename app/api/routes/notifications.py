from fastapi import APIRouter, Depends
import logging
from app.core.security import get_current_user
from app.modules.auth.domain.entity.user import User
from app.modules.notifications.application.request.register_notification_subscriber_request import RegisterNotificationSubscriberRequest
from app.modules.notifications.application.request.update_notification_dubscriber_request import UpdateNotificationSubscriberRequest
from app.modules.notifications.application.use_case.delete_notification import delete_notification_use_case
from app.modules.notifications.application.use_case.delete_notification_subscriber import delete_notification_subscriber_use_case
from app.modules.notifications.application.use_case.get_subscribers import get_subscribers_use_case
from app.modules.notifications.application.use_case.mark_notification_as_read import mark_notification_as_read_use_case
from app.modules.notifications.application.use_case.register_notification_subscriber import register_notification_subscriber_use_case
from app.modules.notifications.application.use_case.update_notification_subscriber import update_notification_subscriber_use_case
from app.modules.notifications.domain.repository.notification_repository_interface import NotificationRepositoryInterface
from app.modules.notifications.infrastructure.dependencies.dependecies import get_notification_repository

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/notifications", tags=["Notifications"])

@router.delete('/subscribers/{subscriber_id}')
async def delete_notification_subscriber(
    subscriber_id: int,
    notification_repository: NotificationRepositoryInterface = Depends(get_notification_repository),
    current_user: User = Depends(get_current_user), 
):
    await delete_notification_subscriber_use_case(
        subscriber_id,
        notification_repository,
    )
    return {"status": "success", "message": f"Subscriber {subscriber_id} deleted successfully."}

@router.post("/subscriber")
async def add_notification_subscriber(
    request: RegisterNotificationSubscriberRequest,
    notification_repository: NotificationRepositoryInterface = Depends(get_notification_repository),
    current_user: User = Depends(get_current_user),
):
    subscriber = await register_notification_subscriber_use_case(
        request,
        notification_repository
    )
    return {"status": "success", "data": subscriber}

@router.get("/subscribers")
async def list_notification_subscribers(
    current_user: User = Depends(get_current_user),
    notification_repository: NotificationRepositoryInterface = Depends(get_notification_repository),
):
    """Get all notification subscribers"""
    subscribers = await get_subscribers_use_case(notification_repository)

    return {"status": "success", "data": subscribers}

@router.patch('/subscribers/{subscriber_id}')
async def update_notification_subscriber(
    subscriber_id: int,
    request: UpdateNotificationSubscriberRequest,
    notification_repository: NotificationRepositoryInterface = Depends(get_notification_repository),
    current_user: User = Depends(get_current_user), 
):
    subscriber = await update_notification_subscriber_use_case(
        subscriber_id,
        request,
        notification_repository
    )
    return {"status": "success", "data": subscriber}

@router.delete('/{notification_id}')
async def delete_notification(
    notification_id: int,
    notification_repository: NotificationRepositoryInterface = Depends(get_notification_repository),
    current_user: User = Depends(get_current_user), 
):
    await delete_notification_use_case(
        notification_id,
        notification_repository,
    )
    return {"status": "success", "message": f"Notification {notification_id} deleted successfully."}

@router.post("/markAsRead/{notification_id}")
async def mark_notification_as_read(
    notification_id: int,
    notification_repository: NotificationRepositoryInterface = Depends(get_notification_repository),
    current_user: User = Depends(get_current_user), 
):
    await mark_notification_as_read_use_case(notification_id, notification_repository)
    return {"status": "success", "message": f"Notification {notification_id} marked as read."}


