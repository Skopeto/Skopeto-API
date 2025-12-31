from app.modules.server_registry.domain.entity.server import Server
from app.core.ssh_client import SSHClientInterface
from abc import ABC, abstractmethod
import logging
import asyncio
from datetime import datetime

logger = logging.getLogger(__name__)

class ServerMetricsServiceInterface(ABC):
    @abstractmethod
    async def get_server_metrics(self, server: Server) -> dict:
        pass

class ServerMetricsService(ServerMetricsServiceInterface):
    def __init__(self, ssh_client: SSHClientInterface):
        self.ssh_client = ssh_client
    
    async def get_server_metrics(self, server: Server) -> dict:
        try:
            async with asyncio.timeout(30):
                self.ssh_client.connect(server)
                
                command = (
                    "top -bn1 | grep 'Cpu(s)' | awk '{print $2}' | cut -d'%' -f1; "
                    "free | grep Mem | awk '{print ($3/$2) * 100.0}'; "
                    "df -h / | tail -1 | awk '{print $5}' | cut -d'%' -f1; "
                    "uptime -p"
                )
                
                output = self.ssh_client.execute_command(command)
                lines = output.strip().split('\n')
                self.ssh_client.disconnect()
                
                def parse_float(value: str) -> float:
                    try:
                        return float(value.replace(',', '.'))
                    except (ValueError, AttributeError):
                        return 0.0
                
                return {
                    'cpu_usage': parse_float(lines[0]) if len(lines) > 0 else 0.0,
                    'memory_usage': parse_float(lines[1]) if len(lines) > 1 else 0.0,
                    'disk_usage': parse_float(lines[2]) if len(lines) > 2 else 0.0,
                    'uptime': lines[3] if len(lines) > 3 else 'unknown',
                    'server_id': server.id,
                    'status': 'healthy',
                    'checked_at': datetime.now()
                }
                
        except asyncio.TimeoutError:
            logger.error(f"Timeout connecting to server {server.user_name} ({server.ip_address})")
            return {
                'cpu_usage': 0.0,
                'memory_usage': 0.0,
                'disk_usage': 0.0,
                'uptime': 'timeout',
                'server_id': server.id,
                'status': 'error',
                'checked_at': datetime.now()
            }
            
        except Exception as e:
            logger.error(f"Failed to get metrics from {server.user_name} ({server.ip_address}): {str(e)}")
            return {
                'cpu_usage': 0.0,
                'memory_usage': 0.0,
                'disk_usage': 0.0,
                'uptime': 'error',
                'server_id': server.id,
                'status': 'offline',
                'checked_at': datetime.now()
            }
        
        finally:
            try:
                self.ssh_client.disconnect()
            except:
                pass