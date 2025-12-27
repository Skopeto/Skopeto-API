# app/core/scheduler.py

import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

logger = logging.getLogger(__name__)

scheduler = AsyncIOScheduler()

async def scheduled_monitoring_task():
    from app.modules.server_registry.application.use_case.collect_and_persist_all_monitoring import collect_and_persist_all_monitoring_use_case
    from app.core.db_session import get_session
    from app.modules.server_registry.infrastructure.sql_repository.server_repository import SqlServerRepository
    from app.modules.docker_registry.infrastructure.sql_repository.docker_repository import SqlDockerRepository
    from app.modules.server_registry.application.service.server_metrics_service import ServerMetricsService
    from app.modules.docker_registry.application.service.docker_metrics_service import DockerMetricService
    from app.core.dependencies import get_ssh_client
    
    logger.info("Starting scheduled monitoring collection...")
    
    try:
        session = await anext(get_session())
        
        server_repo = SqlServerRepository(session)
        docker_repo = SqlDockerRepository(session)
        server_metrics = ServerMetricsService(get_ssh_client())
        docker_metrics = DockerMetricService(get_ssh_client())
        
        results = await collect_and_persist_all_monitoring_use_case(
            server_repo,
            docker_repo,
            server_metrics,
            docker_metrics
        )
        
        await session.commit()
        await session.close()
        
        logger.info(f"Monitoring collection completed. Processed {len(results)} servers")
    except Exception as e:
        logger.error(f"Scheduled monitoring failed: {str(e)}", exc_info=True)
        if session:
            await session.rollback()
            await session.close()

def start_scheduler():
    scheduler.add_job(
        scheduled_monitoring_task,
        trigger=IntervalTrigger(minutes=1),
        id='monitoring_collection',
        name='Collect server and container monitoring data',
        replace_existing=True
    )
    
    scheduler.start()
    logger.info("Scheduler started - monitoring collection will run every 1 hour")

def stop_scheduler():
    if scheduler.running:
        scheduler.shutdown()
        logger.info("Scheduler stopped")