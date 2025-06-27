import logging
from logging.handlers import RotatingFileHandler
from typing import Callable, Optional
import coloredlogs
from .success_level import add_success_log_level


class Logger:
    """
    Standard logger with immediate (synchronous) logging methods.
    Supports deferred (lambda/callable) message evaluation, colored console output, file rotation,
    and a custom SUCCESS log level (green).
    """

    def __init__(
        self,
        name: str = "jgmd2",
        log_file: Optional[str] = None,
        log_level: int = logging.INFO,
        max_bytes: int = 5 * 1024 * 1024,
        backup_count: int = 3,
        colored_console: bool = True,
    ):
        add_success_log_level()
        self.logger = logging.getLogger(name)
        self.logger.setLevel(log_level)
        self._setup_handlers(
            log_file, log_level, max_bytes, backup_count, colored_console
        )

    def _setup_handlers(
        self, log_file, log_level, max_bytes, backup_count, colored_console
    ):
        # Close existing handlers before clearing
        for handler in self.logger.handlers[:]:
            handler.close()
            self.logger.removeHandler(handler)

        if colored_console:
            coloredlogs.install(
                level=log_level,
                logger=self.logger,
                fmt="%(asctime)s %(levelname)s %(name)s %(message)s",
            )
        if log_file:
            file_handler = RotatingFileHandler(
                log_file, maxBytes=max_bytes, backupCount=backup_count
            )
            file_handler.setFormatter(
                logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s")
            )
            self.logger.addHandler(file_handler)

    def close(self):
        """Close all handlers and clean up resources."""
        for handler in self.logger.handlers[:]:
            handler.close()
            self.logger.removeHandler(handler)

    def __del__(self):
        """Destructor to ensure handlers are closed."""
        try:
            self.close()
        except:
            pass

    def log(self, level: str, msg_func: Callable[[], str], *args, **kwargs):
        levelno = (
            logging.getLevelName(level.upper()) if isinstance(level, str) else level
        )
        if self.logger.isEnabledFor(levelno):
            self.logger.log(levelno, msg_func(), *args, **kwargs)

    def debug(self, msg_func: Callable[[], str], *args, **kwargs):
        self.log("DEBUG", msg_func, *args, **kwargs)

    def info(self, msg_func: Callable[[], str], *args, **kwargs):
        self.log("INFO", msg_func, *args, **kwargs)

    def warning(self, msg_func: Callable[[], str], *args, **kwargs):
        self.log("WARNING", msg_func, *args, **kwargs)

    def error(self, msg_func: Callable[[], str], *args, **kwargs):
        self.log("ERROR", msg_func, *args, **kwargs)

    def critical(self, msg_func: Callable[[], str], *args, **kwargs):
        self.log("CRITICAL", msg_func, *args, **kwargs)

    def success(self, msg_func: Callable[[], str], *args, **kwargs):
        self.log("SUCCESS", msg_func, *args, **kwargs)
