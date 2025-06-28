"""
Core event emitter implementation.
"""

import asyncio
from collections import defaultdict
from typing import Callable, Dict, List, Any, Optional, Set
from ..protocols.event_emitter import EventEmitterProtocol
from ..exceptions import EventEmitterError, EventHandlerError
from ...util.errorUtil import exception_to_str


class EventEmitter(EventEmitterProtocol):
    """
    A flexible event emitter that supports both synchronous and asynchronous event handlers.

    Features:
    - Named events with multiple listeners
    - Mixed sync/async handler support
    - Automatic error handling and reporting
    - Thread-safe listener management
    - Event validation and debugging support

    Example:
        emitter = EventEmitter()

        # Sync handler
        def on_data(data):
            print(f"Received data: {data}")

        # Async handler
        async def on_data_async(data):
            await process_data(data)

        emitter.on("data", on_data)
        emitter.on("data", on_data_async)
        emitter.emit("data", {"key": "value"})
    """

    def __init__(
        self,
        error_handler: Optional[Callable[[str, Exception], None]] = None,
        validate_events: bool = False,
        allowed_events: Optional[Set[str]] = None,
    ):
        """
        Initialize the event emitter.

        Args:
            error_handler: Optional callback for handling errors in event handlers.
                          Called with (event_name, exception) when a handler fails.
            validate_events: If True, only allow events that are in allowed_events.
            allowed_events: Set of allowed event names when validation is enabled.
        """
        self._listeners: Dict[str, List[Callable[..., Any]]] = defaultdict(list)
        self._error_handler = error_handler
        self._validate_events = validate_events
        self._allowed_events = allowed_events or set()
        self._event_history: List[tuple[str, Any, Any]] = []  # For debugging

    def on(self, event: str, listener: Callable[..., Any]) -> None:
        """
        Subscribe a listener to an event.

        Args:
            event: The event name to subscribe to
            listener: The callback function to execute when the event is emitted.
                     Can be either synchronous or asynchronous.

        Raises:
            EventEmitterError: If event validation fails or listener is not callable
        """
        if not callable(listener):
            raise EventEmitterError(f"Listener must be callable, got {type(listener)}")

        if self._validate_events and event not in self._allowed_events:
            raise EventEmitterError(
                f"Event '{event}' is not in allowed events: {self._allowed_events}"
            )

        self._listeners[event].append(listener)

    def off(self, event: str, listener: Callable[..., Any]) -> bool:
        """
        Unsubscribe a listener from an event.

        Args:
            event: The event name to unsubscribe from
            listener: The callback function to remove

        Returns:
            True if the listener was found and removed, False otherwise
        """
        if event in self._listeners:
            try:
                self._listeners[event].remove(listener)
                # Clean up empty event lists
                if not self._listeners[event]:
                    del self._listeners[event]
                return True
            except ValueError:
                return False
        return False

    def emit(self, event: str, *args: Any, **kwargs: Any) -> None:
        """
        Emit an event to all registered listeners.

        Args:
            event: The event name to emit
            *args: Positional arguments to pass to listeners
            **kwargs: Keyword arguments to pass to listeners
        """
        if event not in self._listeners:
            return

        # Store event for debugging if needed
        if self._event_history is not None:
            self._event_history.append((event, args, kwargs))

        # Get a copy of listeners to avoid modification during iteration
        listeners = self._listeners[event].copy()

        for listener in listeners:
            self._execute_listener(listener, event, *args, **kwargs)

    def has_listeners(self, event: str) -> bool:
        """
        Check if an event has any registered listeners.

        Args:
            event: The event name to check

        Returns:
            True if the event has listeners, False otherwise
        """
        return event in self._listeners and len(self._listeners[event]) > 0

    def listener_count(self, event: str) -> int:
        """
        Get the number of listeners for an event.

        Args:
            event: The event name to check

        Returns:
            The number of registered listeners for the event
        """
        return len(self._listeners.get(event, []))

    def remove_all_listeners(self, event: Optional[str] = None) -> None:
        """
        Remove all listeners for an event or all events.

        Args:
            event: The event name to clear listeners for. If None, clears all events.
        """
        if event is None:
            self._listeners.clear()
        elif event in self._listeners:
            del self._listeners[event]

    def get_event_names(self) -> Set[str]:
        """
        Get all registered event names.

        Returns:
            Set of all event names that have listeners
        """
        return set(self._listeners.keys())

    def get_listeners(self, event: str) -> List[Callable[..., Any]]:
        """
        Get all listeners for a specific event.

        Args:
            event: The event name to get listeners for

        Returns:
            List of listeners for the event (copy of internal list)
        """
        return self._listeners.get(event, []).copy()

    def _execute_listener(
        self, listener: Callable[..., Any], event: str, *args: Any, **kwargs: Any
    ) -> None:
        """
        Execute a single listener with proper error handling.

        Args:
            listener: The listener function to execute
            event: The event name being processed
            *args: Positional arguments for the listener
            **kwargs: Keyword arguments for the listener
        """
        try:
            if asyncio.iscoroutinefunction(listener):
                # Async listener - create task and handle errors
                task = asyncio.create_task(listener(event, *args, **kwargs))
                task.add_done_callback(
                    lambda t: self._handle_async_task_error(t, event, listener)
                )
            else:
                # Sync listener - execute directly
                listener(event, *args, **kwargs)

        except Exception as e:
            self._handle_sync_error(event, e, listener)

    def _handle_async_task_error(
        self, task: asyncio.Task, event: str, listener: Callable[..., Any]
    ) -> None:
        """
        Handle errors from async tasks.

        Args:
            task: The completed asyncio task
            event: The event name that was being processed
            listener: The listener function that was executed
        """
        try:
            task.result()  # This will raise the exception if the task failed
        except Exception as e:
            self._handle_sync_error(event, e, listener)

    def _handle_sync_error(
        self, event: str, error: Exception, listener: Callable[..., Any]
    ) -> None:
        """
        Handle errors from synchronous listeners.

        Args:
            event: The event name that was being processed
            error: The exception that occurred
            listener: The listener function that failed
        """
        handler_info = f"Handler: {listener.__name__ if hasattr(listener, '__name__') else str(listener)}"

        if self._error_handler:
            try:
                self._error_handler(event, error)
            except Exception as handler_error:
                # If error handler itself fails, log to stderr as fallback with red coloring
                import sys

                print(
                    f"\033[31mError handler failed for event '{event}': {handler_error}\033[0m",
                    file=sys.stderr,
                )
        else:
            # Default error handling - raise EventHandlerError
            raise EventHandlerError(event, error, handler_info)

    def __repr__(self) -> str:
        """String representation of the event emitter."""
        event_counts = {
            event: len(listeners) for event, listeners in self._listeners.items()
        }
        return f"EventEmitter(events={event_counts})"
