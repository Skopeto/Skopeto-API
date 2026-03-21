from fastapi import Depends
from app.modules.database_registry.application.service.database_connector import DatabaseConnector
from app.modules.database_registry.application.service.database_metrics_service import DatabaseMetricsServiceInterface
from app.modules.database_registry.infrastructure.dependencies.dependencies import get_database_connector, get_database_metrics_service
from app.modules.monitoring.application.service.monitoring_orchestration_service import MonitoringOrchestrationService, MonitoringOrchestrationServiceInterface


def get_monitoring_orchestration_service(
    database_metrics: DatabaseMetricsServiceInterface = Depends(get_database_metrics_service),
    connector: DatabaseConnector = Depends(get_database_connector)
) -> MonitoringOrchestrationServiceInterface:
    return MonitoringOrchestrationService(
        database_metrics=database_metrics,
        connector=connector
    )
