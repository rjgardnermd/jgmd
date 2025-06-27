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
from typing import Callable, List, Any, Optional
from .lazy_logger import LazyLogger


class TableLogger(LazyLogger):
    def __init__(self, headers: List[str], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.headers = headers

    def log_row(self, row_func: Callable[[], List[Any]], level: str = "INFO", **kwargs):
        def msg_func():
            row = row_func()
            return tabulate([row], headers=self.headers, tablefmt="grid")

        self.log(level, msg_func, **kwargs)

    def log_table(
        self, rows_func: Callable[[], List[List[Any]]], level: str = "INFO", **kwargs
    ):
        def msg_func():
            rows = rows_func()
            return tabulate(rows, headers=self.headers, tablefmt="grid")

        self.log(level, msg_func, **kwargs)

    def lazy_log_row(
        self, row_func: Callable[[], List[Any]], level: str = "INFO", **kwargs
    ):
        def msg_func():
            row = row_func()
            return tabulate([row], headers=self.headers, tablefmt="grid")

        self.buffer.add(level, msg_func, kwargs)

    def lazy_log_table(
        self, rows_func: Callable[[], List[List[Any]]], level: str = "INFO", **kwargs
    ):
        def msg_func():
            rows = rows_func()
            return tabulate(rows, headers=self.headers, tablefmt="grid")

        self.buffer.add(level, msg_func, kwargs)
