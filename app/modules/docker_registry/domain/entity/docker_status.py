from enum import Enum

class ContainerStatus(str, Enum):
    RUNNING = "running"
    STOPPED = "stopped"
    PAUSED = "paused"
    RESTARTING = "restarting"
    EXITED = "exited"
    CREATED = "created"
    DEAD = "dead"
