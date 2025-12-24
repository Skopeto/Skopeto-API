from abc import ABC, abstractmethod
import paramiko
from typing import Any
from app.modules.server_registry.domain.entity.server import Server
from app.core.encrypt import decrypt_password

class SSHClientInterface(ABC):
    @abstractmethod
    def connect(self, host: str, port: int, username: str, password: str) -> None:
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
    
    def connect(self, host: str, port: int, username: str, password: str) -> None:
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(
            hostname=host,
            port=port,
            username=username,
            password=password,
            timeout=10
        )
    
    def execute_command(self, command: str) -> str:
        if not self.client:
            raise Exception("SSH client not connected")
        
        stdin, stdout, stderr = self.client.exec_command(command)
        output = stdout.read().decode().strip()
        error = stderr.read().decode().strip()
        
        if error:
            raise Exception(f"SSH command failed: {error}")
        
        return output
    
    def disconnect(self) -> None:
        if self.client:
            self.client.close()
            self.client = None