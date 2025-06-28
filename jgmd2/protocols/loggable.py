from typing import Protocol, Optional, Callable, Any


class Loggable(Protocol):
    """Protocol for any object that can log messages."""

    def info(
        self, msg_func: Callable[[], str], color: Optional[Any] = None, **kwargs
    ) -> None: ...
    def debug(
        self, msg_func: Callable[[], str], color: Optional[Any] = None, **kwargs
    ) -> None: ...
    def warning(
        self, msg_func: Callable[[], str], color: Optional[Any] = None, **kwargs
    ) -> None: ...
    def error(
        self, msg_func: Callable[[], str], color: Optional[Any] = None, **kwargs
    ) -> None: ...
    def critical(
        self, msg_func: Callable[[], str], color: Optional[Any] = None, **kwargs
    ) -> None: ...
