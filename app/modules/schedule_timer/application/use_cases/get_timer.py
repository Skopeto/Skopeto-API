from app.modules.schedule_timer.domain.entity.scheduler_timer import SchedulerTimer
from app.modules.schedule_timer.domain.repository.scheduler_timer_repository import SchedulerTimerRepositoryI

async def get_scheduler_timer_use_case(
    repository: SchedulerTimerRepositoryI
) -> SchedulerTimer:
    return await repository.get_timer()
