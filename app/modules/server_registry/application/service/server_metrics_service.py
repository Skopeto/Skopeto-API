from app.modules.server_health_ckeck.domain.entity.heallth_check import ServerCheck
from app.modules.server_registry.domain.entity.server import Server
from app.core.ssh_client import SSHClientInterface
from abc import ABC, abstractmethod
import logging
import asyncio
from datetime import datetime
from app.modules.server_registry.domain.entity.server_check_results import HealthStatus, ServerCheckResults

logger = logging.getLogger(__name__)


def _parse_float(value: str) -> float:
    try:
        return float(value.replace(',', '.'))
    except (ValueError, AttributeError):
        return 0.0


class ServerMetricsServiceInterface(ABC):
    @abstractmethod
    async def get_server_metrics(self, server: Server, server_checks: list[ServerCheck]) -> list[ServerCheckResults]:
        pass


class ServerMetricsService(ServerMetricsServiceInterface):
    def __init__(self, ssh_client: SSHClientInterface):
        self.ssh_client = ssh_client

    async def get_server_metrics(self, server: Server, server_checks: list[ServerCheck]) -> list[ServerCheckResults]:
        results = []

        try:
            async with asyncio.timeout(10):
                self.ssh_client.connect(server)

                for check in server_checks:
                    output = self.ssh_client.execute_command(check.command)
                    lines = output.strip().split('\n')
                    parsed_value = _parse_float(lines[-1]) if lines else 0.0

                    results.append(ServerCheckResults(
                        check_name=check.name,
                        value=parsed_value,
                        unit=check.unit,
                        status=HealthStatus.HEALTHY if parsed_value < check.threshold else HealthStatus.UNHEALTHY,
                        server_id=server.id if server.id else 0,
                        uptime=parsed_value,
                        checked_at=datetime.now(),
                    ))

        except asyncio.TimeoutError:
            logger.error(f"Timeout connecting to server {server.user_name} ({server.ip_address})")
            results = [
                ServerCheckResults(
                    check_name=check.name,
                    value=0.0,
                    unit=check.unit,
                    status=HealthStatus.OFFLINE,
                    server_id=server.id if server.id else 0,
                    uptime=0.0,
                    checked_at=datetime.now(),
                )
                for check in server_checks
            ]

        except Exception as e:
            logger.error(f"Failed to get metrics from {server.user_name} ({server.ip_address}): {str(e)}")
            results = [
                ServerCheckResults(
                    check_name=check.name,
                    value=0.0,
                    unit=check.unit,
                    status=HealthStatus.ERROR,
                    server_id=server.id if server.id else 0,
                    uptime=0.0,
                    checked_at=datetime.now(),
                )
                for check in server_checks
            ]

        finally:
            try:
                self.ssh_client.disconnect()
            except Exception as e:
                logger.warning(f"Failed to disconnect from {server.ip_address}: {str(e)}")

        return results