from typing import NewType, Any

from domain.commands import Command
from domain.events import Event


Message: NewType = Event | Command


class MessageBus:
    def __init__(self, handlers) -> None:
        self._handlers = handlers
    
    def handle(self, message: Message) -> Any:
        queue = [message]
        result = None
        while queue:
            message = queue.pop(0)
            if isinstance(message, Event):
                self._handle_event(message, queue)
            elif isinstance(message, Command):
                result = self._handle_command(message, queue)
            else:
                raise Exception("Not 'Event' or 'Command'")
        return result

    def _handle_event(self, event: Event, queue: list) -> None:
        try:
            for handler in self._handlers[type(event)]:
                handler(event, message_queue=queue)
        except Exception as exception:
            # log exception
            raise

    def _handle_command(self, command: Command, queue: list) -> Any:
        try:
            handler = self._handlers[type(command)]
            result = handler(command, message_queue=queue)
        except Exception as exception:
            # log exception
            raise
        return result
