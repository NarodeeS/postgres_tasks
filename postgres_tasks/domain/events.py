from abc import ABC
from dataclasses import dataclass


class Event(ABC):
    pass


@dataclass
class DbCreated(Event):
    db_name: str
    username: str
    password: str


@dataclass
class TaskDisposed(Event):
    db_name: str
