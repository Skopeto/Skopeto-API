from enum import Enum

class ServerStatus(str, Enum):
    UP = "up"
    DOWN = "down"
    DECOMISSIONED = "decommissioned"
    INACTIVE = "inactive"