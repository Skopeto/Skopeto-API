from app.core.db_session import SessionDep
from app.modules.server_health_ckeck.domain.repository.server_check_repository_interface import ServerCheckRepositoryInterface
from app.modules.server_health_ckeck.infrastructure.sql_repository.server_check_repository import SqlServerCheckRepository


def get_server_check_repository(session: SessionDep) -> ServerCheckRepositoryInterface:
    return SqlServerCheckRepository(session)
