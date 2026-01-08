import logging
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from app.core.db_session import SessionManager
from app.modules.server_registry.infrastructure.sql_repository.server_repository import SqlServerRepository
from app.modules.docker_registry.infrastructure.sql_repository.docker_repository import SqlDockerRepository
from app.modules.notifications.infrastructure.sql_repository.notification_repository import SqlNotificationRepository
from app.modules.notifications.application.service.notification_service import NotificationService
from app.modules.server_registry.application.service.server_metrics_service import ServerMetricsService
from app.modules.docker_registry.application.service.docker_metrics_service import DockerMetricService
from app.modules.server_registry.application.use_case.collect_server_metrics import collect_server_metrics_use_case
from app.modules.docker_registry.application.use_case.collect_container_metrics import collect_container_metrics_use_case
from app.modules.notifications.application.use_case.create_notification_and_notify_subscriber import create_notification_and_notify_subscriber
from app.modules.server_registry.domain.entity.server import Server
from app.core.dependencies import get_ssh_client
from app.core.config import settings

logger = logging.getLogger(__name__)

scheduler = AsyncIOScheduler()

async def scheduled_monitoring_task():
    logger.info("Starting scheduled monitoring collection...")

    # Step 1: fetch servers using ONE short-lived session
    async with SessionManager.session_scope() as session:
        server_repo = SqlServerRepository(session)
        servers = await server_repo.get_all_servers()

    if not servers:
        logger.warning("No servers found for monitoring collection")
        return

    notification_service = NotificationService(
        smtp_host=settings.SMTP_SERVER,
        smtp_port=settings.SMTP_PORT,
        smtp_username=settings.SMTP_USERNAME,
        smtp_password=settings.SMTP_PASSWORD
    )

    server_metrics = ServerMetricsService(get_ssh_client())
    docker_metrics = DockerMetricService(get_ssh_client())

    async def collect_single_server(server: Server):
        if server.id is None:
            return None

        async with SessionManager.session_scope() as session:
            server_repo = SqlServerRepository(session)
            docker_repo = SqlDockerRepository(session)
            notification_repository = SqlNotificationRepository(session)

            try:
                server_health = await collect_server_metrics_use_case(
                    server.id,
                    server_repo,
                    server_metrics
                )

                containers = await collect_container_metrics_use_case(
                    server.id,
                    server,
                    server_health,
                    docker_repo,
                    docker_metrics
                )

                for container in containers:
                    if container.status in {"exited", "dead"}:
                        await create_notification_and_notify_subscriber(
                            message=f"{container.status} status on container {container.name} of server {server.ip_address} {server.user_name}",
                            title="Container Status Alert",
                            notification_repository=notification_repository,
                            notification_service=notification_service
                        )

                if server_health.status in {"unhealthy", "offline", "error"}:
                    await create_notification_and_notify_subscriber(
                        message=f"{server_health.status} status on {server.ip_address} {server.user_name}",
                        title="Server Health Alert",
                        notification_repository=notification_repository,
                        notification_service=notification_service
                    )

                return server.id

            except Exception as e:
                logger.error(f"Failed to collect server {server.id}: {e}", exc_info=True)
                return None

    results = await asyncio.gather(
        *(collect_single_server(server) for server in servers),
        return_exceptions=False
    )

    success_count = len([r for r in results if r is not None])
    logger.info(f"Monitoring collection completed. Processed {success_count}/{len(servers)} servers successfully")

def start_scheduler():
    scheduler.add_job(
        scheduled_monitoring_task,
        trigger=IntervalTrigger(minutes=10),
        id='monitoring_collection',
        name='Collect server and container monitoring data',
        replace_existing=True
    )
    
    scheduler.start()
    logger.info("Scheduler started - monitoring collection will run every {minutes} minute/s")

def stop_scheduler():
    if scheduler.running:
        scheduler.shutdown()
        logger.info("Scheduler stopped")