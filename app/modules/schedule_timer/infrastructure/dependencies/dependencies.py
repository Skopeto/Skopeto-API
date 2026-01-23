from app.modules.schedule_timer.domain.repository.scheduler_timer_repository import SchedulerTimerRepositoryI
from app.modules.schedule_timer.infrastructure.sql_repository.scheduler_timer_repository import SQLSchedulerTimerRepository
from app.core.db_session import SessionDep

async def get_scheduler_timer_repository(session: SessionDep) -> SchedulerTimerRepositoryI:
    return SQLSchedulerTimerRepository(session)