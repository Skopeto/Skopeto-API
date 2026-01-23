from abc import ABC, abstractmethod
from fastapi import WebSocket, WebSocketDisconnect
from app.modules.server_registry.domain.entity.server import Server
from app.core.ssh_client import SSHClientInterface
from app.core.Exception import SSHConnectionException
import asyncio
import logging

logger = logging.getLogger(__name__)

class ServerShellServiceInterface(ABC):
    @abstractmethod
    async def start_interactive_shell(self, websocket: WebSocket, server: Server):
        pass

class ServerShellService(ServerShellServiceInterface):
    def __init__(self, ssh_client: SSHClientInterface):
        self.ssh_client = ssh_client
    
    async def start_interactive_shell(self, websocket: WebSocket, server: Server):
        channel = None
        
        try:
            self.ssh_client.connect(server)
            channel = self.ssh_client.get_shell_channel()
            
            if channel is None:
                raise SSHConnectionException("Failed to create shell channel")
            
            logger.info(f"Shell channel created for {server.ip_address}")
            
            async def read_from_ssh():
                try:
                    while True:
                        if channel.closed or channel.exit_status_ready():
                            logger.info("SSH channel closed or exit detected")
                            await websocket.close()
                            break
                        
                        if channel.recv_ready():
                            data = channel.recv(4096).decode('utf-8', errors='ignore')
                            if data:
                                await websocket.send_json({"type": "output", "data": data})
                        
                        await asyncio.sleep(0.01)
                        
                except WebSocketDisconnect:
                    logger.info("WebSocket disconnected")
                except Exception as e:
                    logger.error(f"Error reading from SSH: {e}")
            
            async def write_to_ssh():
                try:
                    while True:
                        if channel.closed:
                            break
                        
                        message = await websocket.receive_json()
                        
                        if message.get("type") == "input":
                            channel.send(message.get("data", ""))
                        elif message.get("type") == "resize":
                            channel.resize_pty(
                                width=message.get("cols", 80),
                                height=message.get("rows", 24)
                            )
                            
                except WebSocketDisconnect:
                    logger.info("WebSocket disconnected")
                except Exception as e:
                    logger.error(f"Error writing to SSH: {e}")
            
            await asyncio.gather(
                read_from_ssh(),
                write_to_ssh(),
                return_exceptions=True
            )
            
        except SSHConnectionException as e:
            logger.error(f"SSH connection error: {e}")
            try:
                await websocket.send_json({"type": "error", "data": str(e)})
            except:
                pass
        except Exception as e:
            logger.error(f"Shell session error for {server.ip_address}: {e}", exc_info=True)
        finally:
            logger.info(f"Cleaning up shell session for {server.ip_address}")
            try:
                self.ssh_client.disconnect()
            except Exception as e:
                logger.error(f"Error disconnecting: {e}")