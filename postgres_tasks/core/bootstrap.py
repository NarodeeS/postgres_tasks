from core.handlers.message_bus import MessageBus
from core.handlers.handlers import HANDLERS


def bootstrap(handlers: dict | None = HANDLERS) -> MessageBus:
    return MessageBus(handlers)
