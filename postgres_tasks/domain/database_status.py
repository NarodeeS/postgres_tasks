from enum import Enum


class DatabaseStatus(Enum):
    DOWN = "down"
    UP = "up"
    ERROR = 'error'
