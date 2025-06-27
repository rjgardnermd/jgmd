"""
TableLogger: A logger for structured/tabular data, extending LazyLogger.
Supports deferred (lambda/callable) row/table data, immediate and lazy (buffered) logging,
and pretty-prints tables using the 'tabulate' library.
"""

try:
    from tabulate import tabulate
except ImportError:
    raise ImportError(
        "The 'tabulate' library is required for TableLogger. Install it with 'pip install tabulate'."
    )

import logging
from typing import Callable, List, Any, Optional, Union
from .lazy_logger import LazyLogger
from .colors import Colors


class TableLogger(LazyLogger):
    def __init__(
        self,
        headers: List[str],
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
        self.headers = headers

    def log_row(
        self,
        row_func: Callable[[], List[Any]],
        level: str = "INFO",
        color: Optional[Colors] = None,
        **kwargs
    ):
        def msg_func():
            row = row_func()
            return tabulate([row], headers=self.headers, tablefmt="grid")

        self.log(level, msg_func, color=color, **kwargs)

    def log_table(
        self,
        rows_func: Callable[[], List[List[Any]]],
        level: str = "INFO",
        color: Optional[Colors] = None,
        **kwargs
    ):
        def msg_func():
            rows = rows_func()
            return tabulate(rows, headers=self.headers, tablefmt="grid")

        self.log(level, msg_func, color=color, **kwargs)

    def lazy_log_row(
        self,
        row_func: Callable[[], List[Any]],
        level: str = "INFO",
        color: Optional[Colors] = None,
        **kwargs
    ):
        def msg_func():
            row = row_func()
            return tabulate([row], headers=self.headers, tablefmt="grid")

        self.buffer.add(level, msg_func, kwargs, color)

    def lazy_log_table(
        self,
        rows_func: Callable[[], List[List[Any]]],
        level: str = "INFO",
        color: Optional[Colors] = None,
        **kwargs
    ):
        def msg_func():
            rows = rows_func()
            return tabulate(rows, headers=self.headers, tablefmt="grid")

        self.buffer.add(level, msg_func, kwargs, color)
