from abc import ABC, abstractmethod
import paramiko
import logging
from app.core.Exception import SSHConnectionException, SecurityException
from app.modules.server_registry.domain.entity.server import Server
from app.core.encrypt import decrypt_password

logger = logging.getLogger(__name__)

class SSHClientInterface(ABC):
    @abstractmethod
    def connect(self, server: Server) -> None:
        pass
    
    @abstractmethod
    def execute_command(self, command: str) -> str:
        pass
    
    @abstractmethod
    def disconnect(self) -> None:
        pass

class SSHClient(SSHClientInterface):
    def __init__(self):
        self.client = None
    def connect(self, server: Server) -> None:
        try:
            decrypted_password = decrypt_password(server.ssh_password_encrypted)
            
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.client.connect(
                hostname=server.ip_address,
                port=server.port,
                username=server.user_name,
                password=decrypted_password,
                timeout=10
            )
        except paramiko.AuthenticationException as e:
            logger.error(f"SSH authentication failed for {server.ip_address}: {str(e)}", exc_info=True)
            raise SecurityException("Authentication failed")
        except paramiko.SSHException as e:
            logger.error(f"SSH error connecting to {server.ip_address}: {str(e)}", exc_info=True)
            raise SSHConnectionException("Failed to connect to server")
        except Exception as e:
            logger.error(f"Unexpected error connecting to {server.ip_address}: {str(e)}", exc_info=True)
            raise SSHConnectionException("Connection failed")
    
    def execute_command(self, command: str) -> str:
        if not self.client:
            raise SSHConnectionException("Not connected to server")
        
        try:
            stdin, stdout, stderr = self.client.exec_command(command)
            output = stdout.read().decode().strip()
            error = stderr.read().decode().strip()
            
            if error:
                logger.warning(f"Command stderr output: {error}")
                raise SSHConnectionException("Command execution failed")
            
            return output
        except Exception as e:
            logger.error(f"Error executing command '{command}': {str(e)}", exc_info=True)
            raise SSHConnectionException("Command execution failed")
    
    def disconnect(self) -> None:
        if self.client:
            self.client.close()
            self.client = None