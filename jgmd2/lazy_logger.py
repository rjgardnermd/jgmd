import logging
from typing import Callable, Optional, List, Any, Union
from .logger import Logger
from .colors import Colors
from .logLevels import LogLevels


class LazyLogBuffer:
    """
    Buffer for deferred (lazy) log messages. Messages are only logged when flush() is called.
    """

    def __init__(self):
        self._entries: List[tuple[str, Callable[[], str], dict, Optional[Colors]]] = []

    def add(
        self,
        level: LogLevels,
        msg_func: Callable[[], str],
        kwargs: Optional[dict] = None,
        color: Optional[Colors] = None,
    ):
        self._entries.append((level, msg_func, kwargs or {}, color))

    def flush(self, logger: "Logger"):
        for level, msg_func, kwargs, color in self._entries:
            getattr(logger, level.name.lower())(msg_func, color=color, **kwargs)
        self._entries.clear()

    def clear(self):
        self._entries.clear()


class LazyLogger(Logger):
    """
    Logger that buffers log messages and only emits them when flush_lazy() is called.
    Use lazy_debug, lazy_info, lazy_warning, lazy_error, lazy_critical to buffer messages.

    Args:
        sync_mode: If True, lazy_ methods will log synchronously instead of buffering.
                  Useful for debugging without changing code.
    """

    def __init__(
        self,
        name: str = "jgmd2",
        log_directory: Optional[str] = None,
        file_name: Optional[str] = None,
        log_level: LogLevels = LogLevels.INFO,
        max_bytes: int = 5 * 1024 * 1024,
        backup_count: int = 3,
        colored_console: bool = True,
        sync_mode: bool = False,
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
        self.sync_mode = sync_mode

    def lazy_debug(
        self,
        msg_func: Callable[[], str],
        color: Optional[Colors] = None,
        *args,
        **kwargs
    ):
        if self.sync_mode:
            self.debug(msg_func, color=color, **kwargs)
        else:
            self.buffer.add(LogLevels.DEBUG, msg_func, kwargs, color)

    def lazy_info(
        self,
        msg_func: Callable[[], str],
        color: Optional[Colors] = None,
        *args,
        **kwargs
    ):
        if self.sync_mode:
            self.info(msg_func, color=color, **kwargs)
        else:
            self.buffer.add(LogLevels.INFO, msg_func, kwargs, color)

    def lazy_warning(
        self,
        msg_func: Callable[[], str],
        color: Optional[Colors] = None,
        *args,
        **kwargs
    ):
        if self.sync_mode:
            self.warning(msg_func, color=color, **kwargs)
        else:
            self.buffer.add(LogLevels.WARNING, msg_func, kwargs, color)

    def lazy_error(
        self,
        msg_func: Callable[[], str],
        color: Optional[Colors] = None,
        *args,
        **kwargs
    ):
        if self.sync_mode:
            self.error(msg_func, color=color, **kwargs)
        else:
            self.buffer.add(LogLevels.ERROR, msg_func, kwargs, color)

    def lazy_critical(
        self,
        msg_func: Callable[[], str],
        color: Optional[Colors] = None,
        *args,
        **kwargs
    ):
        if self.sync_mode:
            self.critical(msg_func, color=color, **kwargs)
        else:
            self.buffer.add(LogLevels.CRITICAL, msg_func, kwargs, color)

    def lazy_print_header(self, title: str, color: Optional[Colors] = None):
        """
        Buffer a formatted header with the given title (lazy version).

        Args:
            title: The title to display in the header
            color: Optional color for the header (defaults to white)
        """
        header_lines = ["=" * 60, title, "=" * 60]
        header_str = "\n" + "\n".join(header_lines)
        self.lazy_info(lambda: header_str, color=color)
        # for line in header_lines:
        #     self.lazy_info(lambda: line, color=color)

    def flush_lazy(self):
        if not self.sync_mode:
            self.buffer.flush(self)

    def clear_lazy(self):
        if not self.sync_mode:
            self.buffer.clear()
