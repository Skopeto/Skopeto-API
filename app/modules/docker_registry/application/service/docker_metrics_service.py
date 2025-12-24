from app.core.encrypt import decrypt_password
from app.modules.server_registry.domain.entity.server import Server
from app.core.ssh_client import SSHClientInterface
from app.modules.docker_registry.domain.entity.docker_container import DockerContainer

class DockerMetricService:
    def __init__(self, ssh_client: SSHClientInterface):
        self.ssh_client = ssh_client
    
    def get_docker_metrics(self, server: Server) -> list[dict]:
        decrypted_password = decrypt_password(server.ssh_password_encrypted)
        self.ssh_client.connect(server.ip_address, server.port, server.name, decrypted_password)
        
        command = "docker ps --format '{{.ID}}|{{.Names}}|{{.Status}}|{{.Image}}'"
        
        output = self.ssh_client.execute_command(command)
        
        containers = []
        for line in output.strip().split('\n'):
            if line:
                container_id, name, status, image = line.split('|')
                containers.append({
                    'container_id': container_id,
                    'container_name': name,
                    'status': status,
                    'image': image,
                    'server_id': server.id
                })
        
        self.ssh_client.disconnect()
        
        return containers