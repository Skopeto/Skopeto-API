from app.core.scheduler import update_scheduler_interval
from app.modules.schedule_timer.domain.repository.scheduler_timer_repository import SchedulerTimerRepositoryI

async def update_scheduler_timer_use_case(
    interval: int,
    repository: SchedulerTimerRepositoryI
) -> int:
    timer = await repository.get_timer()
    
    if timer:
        result = await repository.update_timer(interval)
    else:
        result = await repository.create_timer(interval)
    
    await update_scheduler_interval(interval)
    
    return result