"""
Protocol definitions for the event emitter system.
"""

from typing import Protocol, Callable, Any, Optional


class EventEmitterProtocol(Protocol):
    """
    Protocol for event emitter implementations.

    This protocol defines the interface that any event emitter must implement,
    allowing for different implementations while maintaining a consistent API.
    """

    def on(self, event: str, listener: Callable[..., Any]) -> None:
        """
        Subscribe a listener to an event.

        Args:
            event: The event name to subscribe to
            listener: The callback function to execute when the event is emitted.
                     Can be either synchronous or asynchronous.
        """
        ...

    def off(self, event: str, listener: Callable[..., Any]) -> bool:
        """
        Unsubscribe a listener from an event.

        Args:
            event: The event name to unsubscribe from
            listener: The callback function to remove

        Returns:
            True if the listener was found and removed, False otherwise
        """
        ...

    def emit(self, event: str, *args: Any, **kwargs: Any) -> None:
        """
        Emit an event to all registered listeners.

        Args:
            event: The event name to emit
            *args: Positional arguments to pass to listeners
            **kwargs: Keyword arguments to pass to listeners
        """
        ...

    def has_listeners(self, event: str) -> bool:
        """
        Check if an event has any registered listeners.

        Args:
            event: The event name to check

        Returns:
            True if the event has listeners, False otherwise
        """
        ...

    def listener_count(self, event: str) -> int:
        """
        Get the number of listeners for an event.

        Args:
            event: The event name to check

        Returns:
            The number of registered listeners for the event
        """
        ...

    def remove_all_listeners(self, event: Optional[str] = None) -> None:
        """
        Remove all listeners for an event or all events.

        Args:
            event: The event name to clear listeners for. If None, clears all events.
        """
        ...
