from abc import ABC, abstractmethod
import asyncio
import paramiko
from typing import Optional
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

    @abstractmethod
    def get_shell_channel(self) -> paramiko.Channel:
        pass

    @abstractmethod
    async def connect_async(self, server: Server) -> None:
        pass

    @abstractmethod
    async def execute_command_async(self, command: str) -> str:
        pass

    @abstractmethod
    async def disconnect_async(self) -> None:
        pass

class SSHClient(SSHClientInterface):
    def __init__(self):
        self.client: Optional[paramiko.SSHClient] = None
        self.channel: Optional[paramiko.Channel] = None
    
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
            logger.info(f"Successfully connected to {server.ip_address}")
            
        except paramiko.AuthenticationException as e:
            logger.error(f"SSH authentication failed for {server.ip_address}: {str(e)}", exc_info=True)
            self.disconnect()
            raise SecurityException("Authentication failed")
        except paramiko.SSHException as e:
            logger.error(f"SSH error connecting to {server.ip_address}: {str(e)}", exc_info=True)
            self.disconnect()
            raise SSHConnectionException("Failed to connect to server")
        except Exception as e:
            logger.error(f"Unexpected error connecting to {server.ip_address}: {str(e)}", exc_info=True)
            self.disconnect()
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
            
            return output
            
        except Exception as e:
            logger.error(f"Error executing command '{command}': {str(e)}", exc_info=True)
            raise SSHConnectionException("Command execution failed")
    
    def get_shell_channel(self) -> paramiko.Channel:
        if not self.client:
            logger.error("Attempted to get shell channel without active client connection")
            raise SSHConnectionException("Not connected to server")
        
        try:
            self.channel = self.client.invoke_shell(
                term='xterm',
                width=80,
                height=24
            )
            
            if self.channel is None:
                logger.error("invoke_shell returned None")
                raise SSHConnectionException("Failed to create shell channel")
            
            self.channel.settimeout(0.0)
            logger.info("Shell channel created and configured successfully")
            return self.channel
            
        except Exception as e:
            logger.error(f"Failed to create shell channel: {str(e)}", exc_info=True)
            self.channel = None
            raise SSHConnectionException(f"Failed to create shell channel: {str(e)}")
    
    def disconnect(self) -> None:
        if self.channel:
            try:
                self.channel.close()
                logger.debug("Shell channel closed")
            except Exception as e:
                logger.warning(f"Error closing channel: {e}")
            finally:
                self.channel = None

        if self.client:
            try:
                self.client.close()
                logger.debug("SSH client disconnected")
            except Exception as e:
                logger.warning(f"Error closing SSH client: {e}")
            finally:
                self.client = None

    async def connect_async(self, server: Server) -> None:
        await asyncio.to_thread(self.connect, server)

    async def execute_command_async(self, command: str) -> str:
        return await asyncio.to_thread(self.execute_command, command)

    async def disconnect_async(self) -> None:
        await asyncio.to_thread(self.disconnect)