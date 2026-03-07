from enum import Enum

class HealthCheckStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"

    