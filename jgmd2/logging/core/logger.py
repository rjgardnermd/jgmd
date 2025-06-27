import logging
from logging.handlers import RotatingFileHandler
from logging import StreamHandler, LogRecord
from typing import Callable, Optional, Union, Dict
import sys

# import os
from datetime import datetime
from ..enums.colors import Colors
from ..enums.log_levels import LogLevels
from typing import TextIO
from ...util import ensure_dir_exists

# def ensure_dir_exists(directory_path: str):
#     """Create directory if it doesn't exist."""
#     if directory_path and not os.path.exists(directory_path):
#         os.makedirs(directory_path)


DEFAULT_COLORS = {
    "DEBUG": Colors.BRIGHT_BLACK,
    "INFO": Colors.BLUE,
    "WARNING": Colors.YELLOW,
    "ERROR": Colors.RED,
    "CRITICAL": Colors.BRIGHT_RED,
}


class ColoredStreamHandler(StreamHandler):
    """Custom stream handler that applies colors to console output with nice formatting."""

    stream: TextIO

    def __init__(self, stream: TextIO = None):
        super().__init__(stream or sys.stdout)

    def setDefaultColors(self, default_colors: Dict[str, Colors]):
        """Set default colors for log levels."""
        self.default_colors = {level: color for level, color in DEFAULT_COLORS.items()}
        if default_colors is not None:
            self.default_colors.update(default_colors)

    def format(self, record: LogRecord):
        """Format the log record with colors for different parts."""
        # Format timestamp
        timestamp = datetime.fromtimestamp(record.created).strftime("%Y-%m-%d %H:%M:%S")
        colored_timestamp = Colors.colorize(timestamp, Colors.GREEN)

        # Format level name with bold and gray, padded to 8 characters for alignment
        level_name = record.levelname.ljust(8)
        colored_level = Colors.colorize(level_name, Colors.BOLD)

        # Format logger name in blue
        colored_name = Colors.colorize(record.name, Colors.BLUE)

        # Format message with default color for the level (or custom color if specified)
        default_color = self.default_colors.get(record.levelname, Colors.WHITE)
        custom_color = getattr(record, "custom_color", None)
        message_color = custom_color if custom_color is not None else default_color
        colored_message = Colors.colorize(record.getMessage(), message_color)

        # Combine all parts
        return f"{colored_timestamp} {colored_level} {colored_name} {colored_message}"

    def emit(self, record: LogRecord):
        try:
            msg = self.format(record)
            self.stream.write(msg + "\n")
            self.flush()
        except Exception:
            self.handleError(record)


class Logger:
    """
    Standard logger with immediate (synchronous) logging methods.
    Supports deferred (lambda/callable) message evaluation, colored console output, file rotation.

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
        log_directory: Optional[str] = None,
        file_name: Optional[str] = None,
        log_level: LogLevels = LogLevels.INFO,
        max_bytes: int = 5 * 1024 * 1024,
        backup_count: int = 3,
        colored_console: bool = True,
        default_colors: Optional[Dict[str, Colors]] = None,
    ):
        log_level = log_level.value
        self.logger = logging.getLogger(name)
        self.logger.setLevel(log_level)
        self.colored_console = colored_console

        # Set up log file path
        if log_directory is not None and file_name is not None:
            ensure_dir_exists(log_directory)
            self.log_file_path = f"{log_directory}/{file_name}"
        else:
            self.log_file_path = None

        self._setup_handlers(
            log_level, max_bytes, backup_count, colored_console, default_colors
        )

    def _setup_handlers(
        self, log_level, max_bytes, backup_count, colored_console, default_colors
    ):
        # Close existing handlers before clearing
        for handler in self.logger.handlers[:]:
            handler.close()
            self.logger.removeHandler(handler)

        if colored_console:
            console_handler = ColoredStreamHandler()
            console_handler.setDefaultColors(default_colors)
            console_handler.setLevel(log_level)
            self.logger.addHandler(console_handler)
        if self.log_file_path:
            file_handler = RotatingFileHandler(
                self.log_file_path, maxBytes=max_bytes, backupCount=backup_count
            )
            file_handler.setFormatter(
                logging.Formatter("%(asctime)s %(levelname)-8s %(name)s %(message)s")
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

    def log(
        self,
        level: LogLevels,
        msg_func: Callable[[], str],
        color: Optional[Colors] = None,
        *args,
        **kwargs,
    ):
        if self.logger.isEnabledFor(level.value):
            message = msg_func()

            # Create a log record
            record = self.logger.makeRecord(
                self.logger.name, level.value, "", 0, message, args, None
            )

            # Add custom color to the record if specified
            if color is not None:
                record.custom_color = color

            # Log the record
            self.logger.handle(record)

    def debug(
        self,
        msg_func: Callable[[], str],
        color: Optional[Colors] = None,
        *args,
        **kwargs,
    ):
        self.log(LogLevels.DEBUG, msg_func, color, *args, **kwargs)

    def info(
        self,
        msg_func: Callable[[], str],
        color: Optional[Colors] = None,
        *args,
        **kwargs,
    ):
        self.log(LogLevels.INFO, msg_func, color, *args, **kwargs)

    def warning(
        self,
        msg_func: Callable[[], str],
        color: Optional[Colors] = None,
        *args,
        **kwargs,
    ):
        self.log(LogLevels.WARNING, msg_func, color, *args, **kwargs)

    def error(
        self,
        msg_func: Callable[[], str],
        color: Optional[Colors] = None,
        *args,
        **kwargs,
    ):
        self.log(LogLevels.ERROR, msg_func, color, *args, **kwargs)

    def critical(
        self,
        msg_func: Callable[[], str],
        color: Optional[Colors] = None,
        *args,
        **kwargs,
    ):
        self.log(LogLevels.CRITICAL, msg_func, color, *args, **kwargs)

    def success(
        self,
        msg_func: Callable[[], str],
        color: Optional[Colors] = Colors.GREEN,
        *args,
        **kwargs,
    ):
        self.log(LogLevels.CRITICAL, msg_func, color, *args, **kwargs)

    def print_header(self, title: str, color: Optional[Colors] = None):
        """
        Print a formatted header with the given title.

        Args:
            title: The title to display in the header
            color: Optional color for the header (defaults to white)
        """
        header_lines = ["=" * 60, title, "=" * 60]
        header_str = "\n" + "\n".join(header_lines)
        self.info(lambda: header_str, color=color)
        # for line in header_lines:
        #     self.info(lambda: line, color=color)
