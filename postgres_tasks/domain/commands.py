from abc import ABC
from dataclasses import dataclass


class Command(ABC):
    pass


@dataclass
class CreateUserTask(Command):
    task_id: int
    user_id: int


@dataclass
class FinishUserTask(Command):
    db_name: str


@dataclass
class DeleteUserTaskDb(Command):
    db_name: str


@dataclass
class SendSqlCommand(Command):
    db_name: str
    query: str


@dataclass
class CheckTask(Command):
    db_name: str
