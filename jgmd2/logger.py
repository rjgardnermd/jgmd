import logging
from logging.handlers import RotatingFileHandler
from typing import Callable, Optional, Union
import coloredlogs
from .success_level import add_success_log_level
from .color_utils import Colors, colorize, get_color_by_name


class Logger:
    """
    Standard logger with immediate (synchronous) logging methods.
    Supports deferred (lambda/callable) message evaluation, colored console output, file rotation,
    and a custom SUCCESS log level (green).

    File Rotation:
        When file rotation is enabled (log_file specified), files are automatically rotated
        when they exceed max_bytes. The naming convention is standard but counterintuitive:
        - log_file (no number) = NEWEST messages (current log file)
        - log_file.1 = Previous rotation (second newest)
        - log_file.2 = Two rotations ago
        - log_file.N = OLDEST messages (oldest backup)
        (Higher numbers = older files, not newer!)
        This is the standard behavior of Python's RotatingFileHandler and most log rotation systems.
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
        self.colored_console = colored_console
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

    def _apply_color(self, message: str, color: Optional[Union[str, Colors]]) -> str:
        """Apply color to message if console output is enabled and color is specified."""
        if not self.colored_console or color is None:
            return message

        if isinstance(color, str):
            try:
                color_code = get_color_by_name(color)
            except ValueError:
                # If it's not a recognized color name, treat it as a color code
                color_code = color
        else:
            color_code = color

        return colorize(message, color_code)

    def log(
        self,
        level: str,
        msg_func: Callable[[], str],
        color: Optional[Union[str, Colors]] = None,
        *args,
        **kwargs
    ):
        levelno = (
            logging.getLevelName(level.upper()) if isinstance(level, str) else level
        )
        if self.logger.isEnabledFor(levelno):
            message = msg_func()
            colored_message = self._apply_color(message, color)
            self.logger.log(levelno, colored_message, *args, **kwargs)

    def debug(
        self,
        msg_func: Callable[[], str],
        color: Optional[Union[str, Colors]] = None,
        *args,
        **kwargs
    ):
        self.log("DEBUG", msg_func, color, *args, **kwargs)

    def info(
        self,
        msg_func: Callable[[], str],
        color: Optional[Union[str, Colors]] = None,
        *args,
        **kwargs
    ):
        self.log("INFO", msg_func, color, *args, **kwargs)

    def warning(
        self,
        msg_func: Callable[[], str],
        color: Optional[Union[str, Colors]] = None,
        *args,
        **kwargs
    ):
        self.log("WARNING", msg_func, color, *args, **kwargs)

    def error(
        self,
        msg_func: Callable[[], str],
        color: Optional[Union[str, Colors]] = None,
        *args,
        **kwargs
    ):
        self.log("ERROR", msg_func, color, *args, **kwargs)

    def critical(
        self,
        msg_func: Callable[[], str],
        color: Optional[Union[str, Colors]] = None,
        *args,
        **kwargs
    ):
        self.log("CRITICAL", msg_func, color, *args, **kwargs)

    def success(
        self,
        msg_func: Callable[[], str],
        color: Optional[Union[str, Colors]] = None,
        *args,
        **kwargs
    ):
        self.log("SUCCESS", msg_func, color, *args, **kwargs)
