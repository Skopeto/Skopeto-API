from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
import logging

from app.modules.schedule_timer.application.use_cases.get_timer import get_scheduler_timer_use_case
from app.modules.schedule_timer.application.use_cases.update_timer import update_scheduler_timer_use_case
from app.modules.schedule_timer.domain.repository.scheduler_timer_repository import SchedulerTimerRepositoryI
from app.modules.schedule_timer.infrastructure.dependencies.dependencies import get_scheduler_timer_repository

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/scheduler", tags=["scheduler"])

class UpdateTimerRequest(BaseModel):
    interval_minutes: int = Field(ge=1, le=1440, description="Interval in minutes (1-1440)")

class TimerResponse(BaseModel):
    interval_minutes: int
    message: str | None = None

@router.get("/timer", response_model=TimerResponse)
async def get_scheduler_timer(
    repository: SchedulerTimerRepositoryI = Depends(get_scheduler_timer_repository)
):
    try:
        timer = await get_scheduler_timer_use_case(repository)
        
        if not timer:
            logger.warning("No timer found in database")
            raise HTTPException(status_code=404, detail="Timer not found. Schedule a new timer.")
        
        return TimerResponse(
            interval_minutes=timer.interval_minutes
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get timer: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to retrieve timer")


@router.put("/timer", response_model=TimerResponse)
async def update_scheduler_timer(
    request: UpdateTimerRequest,
    repository: SchedulerTimerRepositoryI = Depends(get_scheduler_timer_repository)
):
    try:
        interval = await update_scheduler_timer_use_case(request.interval_minutes, repository)
        
        return TimerResponse(
            interval_minutes=interval,
            message=f"Timer updated to {interval} minutes"
        )
    except Exception as e:
        logger.error(f"Failed to update timer: {e}")
        raise HTTPException(status_code=500, detail="Failed to update timer")