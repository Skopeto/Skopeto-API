import time
from datetime import datetime, timezone
from app.modules.database_registry.application.service.database_connector import (
    DatabaseConnector,
)
from app.modules.database_registry.domain.entity.database import Database
from app.modules.database_registry.domain.entity.database_health import (
    DatabaseHealth,
    DatabaseHealthStatus,
)
from abc import ABC, abstractmethod
import logging

logger = logging.getLogger(__name__)


class DatabaseMetricsServiceInterface(ABC):
    @abstractmethod
    async def collect_health(
        self, database: Database, connector: DatabaseConnector
    ) -> dict:
        pass


class DatabaseMetricsService(DatabaseMetricsServiceInterface):
    async def collect_health(
        self, database, connector: DatabaseConnector
    ) -> DatabaseHealth | None:
        if not database.id:
            return None
        try:
            start = time.time()
            connection = await connector.connect(database)
            connection_time_ms = (time.time() - start) * 1000

            start = time.time()
            await connector.execute_test_query(connection, database.db_type)
            query_time_ms = (time.time() - start) * 1000

            await connector.close_connection(connection, database.db_type)

            if connection_time_ms > 5000 or query_time_ms > 5000:
                status = DatabaseHealthStatus.ERROR
            elif connection_time_ms > 1000 or query_time_ms > 1000:
                status = DatabaseHealthStatus.SLOW
            else:
                status = DatabaseHealthStatus.HEALTHY

            return DatabaseHealth(
                database_id=database.id,
                status=status,
                is_connected=True,
                connection_time_ms=connection_time_ms,
                query_time_ms=query_time_ms,
                error_message=None,
                checked_at=datetime.now(timezone.utc),
            )

        except Exception as e:
            return DatabaseHealth(
                database_id=database.id,
                status=DatabaseHealthStatus.OFFLINE,
                is_connected=False,
                connection_time_ms=None,
                query_time_ms=None,
                error_message=str(e),
                checked_at=datetime.now(timezone.utc),
            )
