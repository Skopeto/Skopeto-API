from typing import Any
import logging
from app.core.Exception import RepositoryException
from app.core.base_repository import SqlBaseRepository
from app.core.sql_query import SqlQuery
from app.modules.schedule_timer.domain.entity.scheduler_timer import SchedulerTimer
from app.modules.schedule_timer.domain.repository.scheduler_timer_repository import SchedulerTimerRepositoryI
from app.modules.schedule_timer.infrastructure.sql_query.get_timer_query import create_timer_query, get_timer_query, update_timer_query

logger = logging.getLogger(__name__)

def timer_from_db(row: dict[str, Any] | None) -> SchedulerTimer | None:
    if not row:
        return None
    scheduler_timer_attrs = {
        'id': row['id'],
        'interval_minutes': row['interval_minutes'],
        'created_at': row['created_at']
    }
    return SchedulerTimer.model_construct(**scheduler_timer_attrs)

class SQLSchedulerTimerRepository(SchedulerTimerRepositoryI,SqlBaseRepository):
    async def get_timer(self)-> SchedulerTimer | None:
        try:
            query, params = get_timer_query()
            sql_query = SqlQuery(self.session, query, params)
            return await sql_query.fetch_one(transformer=timer_from_db)
        except Exception as e:
            logger.error(f"Database error while fetching Timer: {str(e)}", exc_info=True)
            raise RepositoryException("Failed to retrieve Timer")

    async def update_timer(self, interval_minutes: int)-> int | None:
        try:
            query, params = update_timer_query(interval_minutes)
            sql_query = SqlQuery(self.session, query, params)
            await sql_query.persist()
            return interval_minutes
        except Exception as e:
            logger.error(f"Database error while updating Timer: {str(e)}", exc_info=True)
            raise RepositoryException("Failed to update Timer")
        
    async def create_timer(self, interval_minutes: int) -> int:
        try:
            query, params = create_timer_query(interval_minutes)
            sql_query = SqlQuery(self.session, query, params)
            await sql_query.persist()
            return interval_minutes
        except Exception as e:
            logger.error(f"create_timer: Error occurred: {str(e)}", exc_info=True)
            raise RepositoryException("Failed to create Timer")