from aiosmtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from asyncssh import logger
import httpx
from abc import ABC, abstractmethod
from app.core.Exception import ApplicationException
from app.modules.notifications.domain.entity.notification_subscriber import NotificationSubscriber

class NotificationServiceInterface(ABC):
    @abstractmethod
    async def send_notification_to_subscribers(
        self, 
        notification_subscriber: NotificationSubscriber, 
        title: str, 
        message: str, 
    ) -> None:
        raise NotImplementedError

class NotificationService(NotificationServiceInterface):
    def __init__(self, smtp_host: str, smtp_port: int, smtp_username: str, smtp_password: str):
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.smtp_username = smtp_username
        self.smtp_password = smtp_password
    
    async def send_email(self, to_email: str, subject: str, body: str) -> None:
        msg = MIMEMultipart()
        msg['From'] = self.smtp_username
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        
        async with SMTP(hostname=self.smtp_host, port=self.smtp_port) as smtp:
            await smtp.login(self.smtp_username, self.smtp_password)
            await smtp.send_message(msg)
    
    async def send_slack_notification(self, webhook_url: str, message: str) -> None:
        async with httpx.AsyncClient() as client:
            payload = {"text": message}
            response = await client.post(webhook_url, json=payload)
            if response.status_code != 200:
                raise ApplicationException(f"Failed to send Slack notification: {response.status_code}")
    
    async def send_notification_to_subscribers(
        self, 
        notification_subscriber: NotificationSubscriber, 
        title: str, 
        message: str, 
    ) -> None:
        if notification_subscriber.notification_channel == "email":
            if notification_subscriber.delivery_address_email:
                await self.send_email(notification_subscriber.delivery_address_email, title, message)
            else:
                logger.warning(f"Skipping email notification for subscriber {notification_subscriber.user_id}: no email set")
        elif notification_subscriber.notification_channel == "slack":
            if notification_subscriber.slack_webhook_url:
                await self.send_slack_notification(notification_subscriber.slack_webhook_url, message)
            else:
                logger.warning(f"Skipping Slack notification for subscriber {notification_subscriber.user_id}: no webhook URL set")
        else:
            raise ApplicationException(f"Unsupported notification channel: {notification_subscriber.notification_channel}")