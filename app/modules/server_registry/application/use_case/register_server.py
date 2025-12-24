from app.modules.server_registry.application.request.register_server_location_request import RegisterServerLocationRequest
from app.modules.server_registry.domain.entity.server import Server
from argon2 import PasswordHasher
from app.modules.server_registry.domain.entity.server_status import ServerStatus
from app.modules.server_registry.domain.repository.server_repository import ServerRepositoryInterface
from app.core.encrypt import encrypt_password

password_hasher = PasswordHasher()

def hash_password(password: str) -> str:
    truncated = password[:72]
    return password_hasher.hash(truncated)

def register_server_use_case(request: RegisterServerLocationRequest, server_repository: ServerRepositoryInterface) -> Server:
    server = Server(
        name=request.name,
        ssh_password_encrypted=encrypt_password(request.password),
        ip_address=str(request.ip_address),
        port=request.port,
        status=request.status
    )
    return server_repository.persist_server(server)