from app.modules.server_registry.domain.entity.server import Server
from app.core.ssh_client import SSHClientInterface
import logging

logger = logging.getLogger(__name__)

class DockerMetricService:  # Fixed: was DockerMetricsService
    def __init__(self, ssh_client: SSHClientInterface):
        self.ssh_client = ssh_client
    
    def get_docker_metrics(self, server: Server) -> list[dict]:
        try:
            self.ssh_client.connect(server)
            
            # Add {{.Ports}} to the format
            command = "docker ps --format '{{.ID}}|{{.Names}}|{{.Status}}|{{.Image}}|{{.Ports}}'"
            output = self.ssh_client.execute_command(command)
            
            containers = []
            for line in output.strip().split('\n'):
                if line:
                    parts = line.split('|')
                    if len(parts) == 5:  # Now expecting 5 parts
                        container_id, name, status, image, ports = parts
                        containers.append({
                            'container_id': container_id,
                            'name': name, 
                            'status': self._parse_status(status), 
                            'image': image,
                            'ports': ports,  # Add this
                            'server_id': server.id
                        })
            
            logger.info(f"Found {len(containers)} containers on {server.ip_address}")
            self.ssh_client.disconnect()
            return containers
        except Exception as e:
            logger.error(f"Failed to get Docker metrics: {e}", exc_info=True)
            self.ssh_client.disconnect()
            return []
    
    def _parse_status(self, status_str: str) -> str:  # Indent this inside the class
        if status_str.startswith('Up'):
            return 'running'
        elif 'Exited' in status_str:
            return 'exited'
        elif 'Paused' in status_str:
            return 'paused'
        else:
            return 'stopped'