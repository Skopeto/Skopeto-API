import datetime
from typing import Any
import logging
from app.core.Exception import RepositoryException
from app.core.base_repository import SqlBaseRepository
from app.core.sql_query import SqlQuery
from app.modules.database_registry.domain.entity.database import Database
from app.modules.database_registry.domain.entity.database_health import DatabaseHealth
from app.modules.database_registry.domain.repository.database_repository import (
    DatabaseRepositoryInterface,
)
from app.modules.database_registry.infrastructure.sql_query.sql_database_query import (
    create_database_health_query,
    create_database_query,
    get_database_by_id_query,
    get_database_by_name_query,
    get_database_health_query,
    get_databases_query,
    update_database_health_query,
    update_database_query,
)

logger = logging.getLogger(__name__)


def database_from_db(row: dict[str, Any] | None) -> Database | None:
    if not row:
        return None

    database_attrs = {
        "id": row["id"],
        "server_id": row["server_id"],
        "name": row["name"],
        "db_type": row["db_type"],
        "host": row["host"],
        "port": row["port"],
        "database_name": row["database_name"],
        "service_name": row["service_name"],
        "username": row["username"],
        "encrypted_password": row["encrypted_password"],
        "created_at": row["created_at"].replace(tzinfo=datetime.timezone.utc),
    }
    return Database.model_construct(**database_attrs)


def database_health_from_db(row: dict[str, Any] | None) -> DatabaseHealth | None:
    if not row:
        return None

    # Add UTC timezone to naive datetime from database
    checked_at = row["checked_at"]
    if checked_at and checked_at.tzinfo is None:
        checked_at = checked_at.replace(tzinfo=datetime.timezone.utc)

    database_health_attrs = {
        "id": row["id"],
        "database_id": row["database_id"],
        "status": row["status"],
        "connection_time_ms": row["connection_time_ms"],
        "is_connected": row["is_connected"],
        "query_time_ms": row["query_time_ms"],
        "error_message": row["error_message"],
        "checked_at": checked_at,
    }
    return DatabaseHealth.model_construct(**database_health_attrs)


class SqlDatabaseRepository(DatabaseRepositoryInterface, SqlBaseRepository):
    async def get_databases_by_server_id(self, server_id: int) -> list[Database] | None:
        try:
            query, params = get_databases_query(server_id)
            sql_query = SqlQuery(self.session, query, params)
            rows = await sql_query.fetch_all()
            databases = [database_from_db(row) for row in rows]
            return list(filter(None, databases))
        except Exception as e:
            logger.error(
                f"Database error while fetching databse with server ID {server_id}: {str(e)}",
                exc_info=True,
            )
            raise RepositoryException("Failed to fetch databases by server ID")

    async def persist_database(self, database: Database) -> Database:
        try:
            query, params = create_database_query(database)
            sql_query = SqlQuery(self.session, query, params)
            await sql_query.persist()
            return database
        except Exception as e:
            logger.error(
                f"Database error while persisting database {database.name}: {str(e)}",
                exc_info=True,
            )
            raise RepositoryException("Failed to persist database")

    async def get_database_by_name(self, name: str) -> Database | None:
        try:
            query, params = get_database_by_name_query(name)
            sql_query = SqlQuery(self.session, query, params)
            return await sql_query.fetch_one(transformer=database_from_db)
        except Exception as e:
            logger.error(
                f"Database error while fetching database with name {name}: {str(e)}",
                exc_info=True,
            )
            raise RepositoryException("Failed to fetch database by name")

    async def persist_database_health(
        self, database_health: DatabaseHealth
    ) -> DatabaseHealth:
        try:
            query, params = create_database_health_query(database_health)
            sql_query = SqlQuery(self.session, query, params)
            await sql_query.persist()
            return database_health
        except Exception as e:
            logger.error(
                f"Database error while saving database health for database {database_health.database_id}: {str(e)}",
                exc_info=True,
            )
            raise RepositoryException("Failed to save database health")

    async def get_database_health(self, database_id: int) -> DatabaseHealth | None:
        try:
            query, params = get_database_health_query(database_id)
            sql_query = SqlQuery(self.session, query, params)
            database_health = await sql_query.fetch_one(
                transformer=database_health_from_db
            )
            return database_health
        except Exception as e:
            logger.error(
                f"Database error while fetching database health {database_id}: {str(e)}",
                exc_info=True,
            )
            raise RepositoryException("Failed to retrieve database health")

    async def update_database_health(
        self, database_health: DatabaseHealth
    ) -> DatabaseHealth:
        try:
            query, params = update_database_health_query(database_health)
            sql_query = SqlQuery(self.session, query, params)
            await sql_query.persist()
            return database_health
        except Exception as e:
            logger.error(
                f"Database error while updating database health {database_health.id}: {str(e)}",
                exc_info=True,
            )
            raise RepositoryException("Failed to update database health")

    async def update_database(self, database: Database) -> Database:
        try:
            query, params = update_database_query(database)
            sql_query = SqlQuery(self.session, query, params)
            await sql_query.persist()
            return database
        except Exception as e:
            logger.error(
                f"Database error while updating database {database.id}: {str(e)}",
                exc_info=True,
            )
            raise RepositoryException("Failed to update database")
        
    async def delete_database(self, database_id: int) -> None:
        try:
            query = """
            DELETE FROM databases
            WHERE id = :database_id
            """
            params = {"database_id": database_id}
            sql_query = SqlQuery(self.session, query, params)
            await sql_query.persist()
        except Exception as e:
            logger.error(
                f"Database error while deleting database {database_id}: {str(e)}",
                exc_info=True,
            )
            raise RepositoryException("Failed to delete database")
    
    async def get_database_by_id(self, database_id: int) -> Database | None:
        try:
            query, params = get_database_by_id_query(database_id)
            sql_query = SqlQuery(self.session, query, params)
            database = await sql_query.fetch_one(transformer=database_from_db)
            return database
        except Exception as e:
            logger.error(
                f"Database error while fetching database with ID {database_id}: {str(e)}",
                exc_info=True,
            )
            raise RepositoryException("Failed to fetch database by ID")

