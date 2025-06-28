"""
Custom exceptions for the event emitter system.
"""


class EventEmitterError(Exception):
    """Base exception for event emitter errors."""

    pass


class EventHandlerError(EventEmitterError):
    """Exception raised when an event handler encounters an error."""

    def __init__(self, event: str, error: Exception, handler_info: str = ""):
        self.event = event
        self.original_error = error
        self.handler_info = handler_info
        super().__init__(f"Error in event handler for '{event}': {error}")
