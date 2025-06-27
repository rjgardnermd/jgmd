import logging
from logging.handlers import RotatingFileHandler
from typing import Callable, Optional, List, Any, Union
from .logger import Logger
from .color_utils import Colors


class LazyLogBuffer:
    """
    Buffer for deferred (lazy) log messages. Messages are only logged when flush() is called.
    """

    def __init__(self):
        self._entries: List[
            tuple[str, Callable[[], str], dict, Optional[Union[str, Colors]]]
        ] = []

    def add(
        self,
        level: str,
        msg_func: Callable[[], str],
        kwargs: Optional[dict] = None,
        color: Optional[Union[str, Colors]] = None,
    ):
        self._entries.append((level, msg_func, kwargs or {}, color))

    def flush(self, logger: "Logger"):
        for level, msg_func, kwargs, color in self._entries:
            getattr(logger, level.lower())(msg_func, color=color, **kwargs)
        self._entries.clear()

    def clear(self):
        self._entries.clear()


class LazyLogger(Logger):
    """
    Logger that buffers log messages and only emits them when flush_lazy() is called.
    Use lazy_debug, lazy_info, lazy_warning, lazy_error, lazy_critical to buffer messages.
    """

    def __init__(
        self,
        name: str = "jgmd2",
        log_directory: Optional[str] = None,
        file_name: Optional[str] = None,
        log_level: int = logging.INFO,
        max_bytes: int = 5 * 1024 * 1024,
        backup_count: int = 3,
        colored_console: bool = True,
    ):
        super().__init__(
            name=name,
            log_directory=log_directory,
            file_name=file_name,
            log_level=log_level,
            max_bytes=max_bytes,
            backup_count=backup_count,
            colored_console=colored_console,
        )
        self.buffer = LazyLogBuffer()

    def lazy_debug(
        self,
        msg_func: Callable[[], str],
        color: Optional[Union[str, Colors]] = None,
        *args,
        **kwargs
    ):
        self.buffer.add("DEBUG", msg_func, kwargs, color)

    def lazy_info(
        self,
        msg_func: Callable[[], str],
        color: Optional[Union[str, Colors]] = None,
        *args,
        **kwargs
    ):
        self.buffer.add("INFO", msg_func, kwargs, color)

    def lazy_warning(
        self,
        msg_func: Callable[[], str],
        color: Optional[Union[str, Colors]] = None,
        *args,
        **kwargs
    ):
        self.buffer.add("WARNING", msg_func, kwargs, color)

    def lazy_error(
        self,
        msg_func: Callable[[], str],
        color: Optional[Union[str, Colors]] = None,
        *args,
        **kwargs
    ):
        self.buffer.add("ERROR", msg_func, kwargs, color)

    def lazy_critical(
        self,
        msg_func: Callable[[], str],
        color: Optional[Union[str, Colors]] = None,
        *args,
        **kwargs
    ):
        self.buffer.add("CRITICAL", msg_func, kwargs, color)

    def lazy_print_header(self, title: str, color: Optional[Union[str, Colors]] = None):
        """
        Buffer a formatted header with the given title (lazy version).

        Args:
            title: The title to display in the header
            color: Optional color for the header (defaults to white)
        """
        header_lines = ["=" * 60, title, "=" * 60]

        for line in header_lines:
            self.lazy_info(lambda: line, color=color)

    def flush_lazy(self):
        self.buffer.flush(self)

    def clear_lazy(self):
        self.buffer.clear()


# Example usage (to be removed or moved to docs/tests):
# logger = LazyLogger("myapp", log_file="myapp.log", log_level=logging.DEBUG)
# logger.debug(lambda: f"Debug value: {expensive_func()}")
# logger.success(lambda: "Operation completed successfully!")
# logger.lazy_info(lambda: f"Deferred info: {expensive_func()}")
# logger.lazy_success(lambda: "Deferred success!")
# logger.flush_lazy()
