from fastapi import Depends
from app.modules.database_registry.application.service.database_connector import DatabaseConnector
from app.modules.database_registry.application.service.database_metrics_service import DatabaseMetricsServiceInterface
from app.modules.database_registry.infrastructure.dependencies.dependencies import get_database_connector, get_database_metrics_service
from app.modules.docker_registry.application.service.docker_metrics_service import DockerMetricService
from app.modules.docker_registry.infrastructure.dependencies.dependencies import get_docker_metrics_service
from app.modules.monitoring.application.service.monitoring_orchestration_service import MonitoringOrchestrationService, MonitoringOrchestrationServiceInterface
from app.modules.server_registry.application.service.server_metrics_service import ServerMetricsServiceInterface
from app.modules.server_registry.infrastructure.dependencies.dependencies import get_server_metrics_service


def get_monitoring_orchestration_service(
    server_metrics: ServerMetricsServiceInterface = Depends(get_server_metrics_service),
    docker_metrics: DockerMetricService = Depends(get_docker_metrics_service),
    database_metrics: DatabaseMetricsServiceInterface = Depends(get_database_metrics_service),
    connector: DatabaseConnector = Depends(get_database_connector)
) -> MonitoringOrchestrationServiceInterface:
    return MonitoringOrchestrationService(
        server_metrics=server_metrics,
        docker_metrics=docker_metrics,
        database_metrics=database_metrics,
        connector=connector
    )
