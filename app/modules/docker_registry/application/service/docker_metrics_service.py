from app.modules.server_registry.domain.entity.server import Server
from app.core.ssh_client import SSHClientInterface
from app.modules.docker_registry.domain.entity.docker_status import ContainerStatus
import logging
import re
import asyncio

logger = logging.getLogger(__name__)

class DockerMetricService:
    def __init__(self, ssh_client: SSHClientInterface):
        self.ssh_client = ssh_client
    
    async def get_docker_metrics(self, server: Server) -> list[dict]:
        try:
            async with asyncio.timeout(30):
                self.ssh_client.connect(server)
                
                command = "docker ps -a --format '{{.ID}}|{{.Names}}|{{.Status}}|{{.State}}|{{.Image}}|{{.Ports}}'"
                output = self.ssh_client.execute_command(command)
                
                containers = []
                for line in output.strip().split('\n'):
                    if line:
                        parts = line.split('|')
                        if len(parts) >= 6:
                            container_id, name, status_str, state, image, ports = parts[:6]
                            status, exit_code, is_healthy = self._parse_status(status_str, state)
                            
                            containers.append({
                                'container_id': container_id.strip(),
                                'name': name.strip(),
                                'status': status,
                                'image': image.strip(),
                                'ports': ports.strip() if ports else '',
                                'server_id': server.id,
                                'exit_code': exit_code,
                                'is_healthy': is_healthy,
                                'state_changed_at': None
                            })
                
                logger.info(f"Found {len(containers)} containers on {server.ip_address}")
                return containers
                
        except asyncio.TimeoutError:
            logger.error(f"Timeout getting Docker metrics from {server.user_name} ({server.ip_address})")
            return []
            
        except Exception as e:
            logger.error(f"Failed to get Docker metrics from {server.user_name}: {e}", exc_info=True)
            return []
            
        finally:
            try:
                self.ssh_client.disconnect()
            except:
                pass
    
    def _parse_status(self, status_str: str, state: str) -> tuple[ContainerStatus, int | None, bool | None]:
        state_lower = state.lower()
        exit_code = None
        
        if state_lower == "exited":
            match = re.search(r'Exited \((\d+)\)', status_str)
            if match:
                exit_code = int(match.group(1))
        
        is_healthy = None
        if "(healthy)" in status_str.lower():
            is_healthy = True
        elif "(unhealthy)" in status_str.lower():
            is_healthy = False
        
        status_map = {
            "running": ContainerStatus.RUNNING,
            "exited": ContainerStatus.EXITED,
            "paused": ContainerStatus.PAUSED,
            "restarting": ContainerStatus.RESTARTING,
            "created": ContainerStatus.CREATED,
            "dead": ContainerStatus.DEAD,
        }
        
        container_status = status_map.get(state_lower, ContainerStatus.STOPPED)
        return container_status, exit_code, is_healthy