import pytest
from unittest.mock import AsyncMock
from datetime import datetime, timezone

from app.modules.database_registry.application.use_case.collect_database_health import (
    collect_databases_for_server_use_case,
    DatabaseWithHealth,
)
from app.modules.database_registry.domain.entity.database import Database
from app.modules.database_registry.domain.entity.database_health import DatabaseHealth, DatabaseHealthStatus


@pytest.mark.asyncio
async def test_collect_databases_for_server_success(
    mock_database_repository: AsyncMock,
    mock_database_metrics_service: AsyncMock,
    mock_database_connector: AsyncMock,
    sample_database: Database,
    sample_database_health: DatabaseHealth
):
    """Test successful collection of database health for a server"""
    # Arrange
    server_id = 1
    mock_database_repository.get_databases_by_server_id.return_value = [sample_database]
    mock_database_metrics_service.collect_health.return_value = sample_database_health
    mock_database_repository.get_database_health.return_value = None  # No existing health
    mock_database_repository.persist_database_health.return_value = sample_database_health

    # Act
    result = await collect_databases_for_server_use_case(
        server_id=server_id,
        database_repo=mock_database_repository,
        database_metrics=mock_database_metrics_service,
        connector=mock_database_connector
    )

    # Assert
    assert len(result) == 1
    assert isinstance(result[0], DatabaseWithHealth)
    assert result[0].database.id == sample_database.id
    assert result[0].database_health.database_id == sample_database_health.database_id
    assert result[0].database_health.status == DatabaseHealthStatus.HEALTHY

    mock_database_repository.get_databases_by_server_id.assert_called_once_with(server_id)
    mock_database_metrics_service.collect_health.assert_called_once_with(sample_database, mock_database_connector)
    mock_database_repository.get_database_health.assert_called_once_with(sample_database.id)
    mock_database_repository.persist_database_health.assert_called_once_with(sample_database_health)
    mock_database_repository.update_database_health.assert_not_called()


@pytest.mark.asyncio
async def test_collect_databases_for_server_with_existing_health(
    mock_database_repository: AsyncMock,
    mock_database_metrics_service: AsyncMock,
    mock_database_connector: AsyncMock,
    sample_database: Database,
    sample_database_health: DatabaseHealth
):
    """Test collection when database health already exists (should update instead of persist)"""
    # Arrange
    server_id = 1
    existing_health = DatabaseHealth(
        id=1,
        database_id=1,
        status=DatabaseHealthStatus.HEALTHY,
        connection_time_ms=60.0,
        is_connected=True,
        query_time_ms=30.0,
        error_message=None,
        checked_at=datetime(2025, 12, 25, 12, 0, 0, tzinfo=timezone.utc)
    )

    mock_database_repository.get_databases_by_server_id.return_value = [sample_database]
    mock_database_metrics_service.collect_health.return_value = sample_database_health
    mock_database_repository.get_database_health.return_value = existing_health  # Health exists
    mock_database_repository.update_database_health.return_value = sample_database_health

    # Act
    result = await collect_databases_for_server_use_case(
        server_id=server_id,
        database_repo=mock_database_repository,
        database_metrics=mock_database_metrics_service,
        connector=mock_database_connector
    )

    # Assert
    assert len(result) == 1
    mock_database_repository.update_database_health.assert_called_once_with(sample_database_health)
    mock_database_repository.persist_database_health.assert_not_called()


@pytest.mark.asyncio
async def test_collect_databases_for_server_multiple_databases(
    mock_database_repository: AsyncMock,
    mock_database_metrics_service: AsyncMock,
    mock_database_connector: AsyncMock,
    sample_database: Database
):
    """Test collection for multiple databases"""
    # Arrange
    server_id = 1

    database2 = Database(
        id=2,
        server_id=1,
        name="second-database",
        db_type="mysql",
        host="mysql.example.com",
        port=3306,
        database_name="mysqldb",
        service_name=None,
        username="mysqluser",
        encrypted_password="encrypted_password2",
        created_at=datetime(2025, 12, 26, 13, 0, 0, tzinfo=timezone.utc)
    )

    health1 = DatabaseHealth(
        id=1,
        database_id=1,
        status=DatabaseHealthStatus.HEALTHY,
        connection_time_ms=50.5,
        is_connected=True,
        query_time_ms=25.3,
        error_message=None,
        checked_at=datetime(2025, 12, 26, 12, 0, 0, tzinfo=timezone.utc)
    )

    health2 = DatabaseHealth(
        id=2,
        database_id=2,
        status=DatabaseHealthStatus.SLOW,
        connection_time_ms=150.0,
        is_connected=True,
        query_time_ms=200.0,
        error_message=None,
        checked_at=datetime(2025, 12, 26, 12, 0, 0, tzinfo=timezone.utc)
    )

    mock_database_repository.get_databases_by_server_id.return_value = [sample_database, database2]
    mock_database_metrics_service.collect_health.side_effect = [health1, health2]
    mock_database_repository.get_database_health.return_value = None
    mock_database_repository.persist_database_health.side_effect = [health1, health2]

    # Act
    result = await collect_databases_for_server_use_case(
        server_id=server_id,
        database_repo=mock_database_repository,
        database_metrics=mock_database_metrics_service,
        connector=mock_database_connector
    )

    # Assert
    assert len(result) == 2
    assert result[0].database.id == 1
    assert result[0].database_health.status == DatabaseHealthStatus.HEALTHY
    assert result[1].database.id == 2
    assert result[1].database_health.status == DatabaseHealthStatus.SLOW

    assert mock_database_metrics_service.collect_health.call_count == 2
    assert mock_database_repository.persist_database_health.call_count == 2


@pytest.mark.asyncio
async def test_collect_databases_for_server_empty_list(
    mock_database_repository: AsyncMock,
    mock_database_metrics_service: AsyncMock,
    mock_database_connector: AsyncMock
):
    """Test collection when no databases exist for a server"""
    # Arrange
    server_id = 999
    mock_database_repository.get_databases_by_server_id.return_value = []

    # Act
    result = await collect_databases_for_server_use_case(
        server_id=server_id,
        database_repo=mock_database_repository,
        database_metrics=mock_database_metrics_service,
        connector=mock_database_connector
    )

    # Assert
    assert result == []
    mock_database_repository.get_databases_by_server_id.assert_called_once_with(server_id)
    mock_database_metrics_service.collect_health.assert_not_called()
    mock_database_repository.persist_database_health.assert_not_called()
    mock_database_repository.update_database_health.assert_not_called()


@pytest.mark.asyncio
async def test_collect_databases_for_server_skip_databases_without_id(
    mock_database_repository: AsyncMock,
    mock_database_metrics_service: AsyncMock,
    mock_database_connector: AsyncMock,
    sample_database: Database
):
    """Test that databases without ID are skipped"""
    # Arrange
    server_id = 1

    # Database without ID (shouldn't happen in practice but let's test defensive code)
    database_without_id = Database(
        id=None,
        server_id=1,
        name="incomplete-database",
        db_type="postgresql",
        host="localhost",
        port=5432,
        database_name="testdb",
        service_name=None,
        username="testuser",
        encrypted_password="encrypted_password",
        created_at=datetime(2025, 12, 26, 12, 0, 0, tzinfo=timezone.utc)
    )

    health1 = DatabaseHealth(
        id=1,
        database_id=1,
        status=DatabaseHealthStatus.HEALTHY,
        connection_time_ms=50.5,
        is_connected=True,
        query_time_ms=25.3,
        error_message=None,
        checked_at=datetime(2025, 12, 26, 12, 0, 0, tzinfo=timezone.utc)
    )

    mock_database_repository.get_databases_by_server_id.return_value = [sample_database, database_without_id]
    mock_database_metrics_service.collect_health.return_value = health1
    mock_database_repository.get_database_health.return_value = None
    mock_database_repository.persist_database_health.return_value = health1

    # Act
    result = await collect_databases_for_server_use_case(
        server_id=server_id,
        database_repo=mock_database_repository,
        database_metrics=mock_database_metrics_service,
        connector=mock_database_connector
    )

    # Assert
    assert len(result) == 1
    assert result[0].database.id == 1
    # collect_health should only be called once for the database with an ID
    mock_database_metrics_service.collect_health.assert_called_once()


@pytest.mark.asyncio
async def test_collect_databases_for_server_with_database_errors(
    mock_database_repository: AsyncMock,
    mock_database_metrics_service: AsyncMock,
    mock_database_connector: AsyncMock,
    sample_database: Database
):
    """Test collection when database is in error state"""
    # Arrange
    server_id = 1

    error_health = DatabaseHealth(
        id=1,
        database_id=1,
        status=DatabaseHealthStatus.ERROR,
        connection_time_ms=None,
        is_connected=False,
        query_time_ms=None,
        error_message="Connection refused",
        checked_at=datetime(2025, 12, 26, 12, 0, 0, tzinfo=timezone.utc)
    )

    mock_database_repository.get_databases_by_server_id.return_value = [sample_database]
    mock_database_metrics_service.collect_health.return_value = error_health
    mock_database_repository.get_database_health.return_value = None
    mock_database_repository.persist_database_health.return_value = error_health

    # Act
    result = await collect_databases_for_server_use_case(
        server_id=server_id,
        database_repo=mock_database_repository,
        database_metrics=mock_database_metrics_service,
        connector=mock_database_connector
    )

    # Assert
    assert len(result) == 1
    assert result[0].database_health.status == DatabaseHealthStatus.ERROR
    assert result[0].database_health.is_connected is False
    assert result[0].database_health.error_message == "Connection refused"
    mock_database_repository.persist_database_health.assert_called_once_with(error_health)
