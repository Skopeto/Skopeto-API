from abc import ABC, abstractmethod

from app.modules.schedule_timer.domain.entity.scheduler_timer import SchedulerTimer

class SchedulerTimerRepositoryI(ABC):
    @abstractmethod
    async def get_timer(self) -> SchedulerTimer:
        pass

    @abstractmethod
    async def update_timer(self, interval: int) -> int:
        pass

    @abstractmethod
    async def create_timer(self, interval: int) -> int:
        pass