from app.core.ssh_client import SSHClientInterface, SSHClient

def get_ssh_client() -> SSHClientInterface:
    return SSHClient()