"""
Color utilities for jgmd2 logging framework.
Provides color constants and functions to apply colors to log messages.
"""


class Colors:
    """ANSI color codes for terminal output."""

    # Standard colors
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"

    # Bright colors
    BRIGHT_BLACK = "\033[90m"
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"
    BRIGHT_WHITE = "\033[97m"

    # Formatting
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    RESET = "\033[0m"


def colorize(text: str, color: str) -> str:
    """
    Apply color to text.

    Args:
        text: The text to colorize
        color: Color code from Colors class

    Returns:
        Colorized text with reset at the end
    """
    return f"{color}{text}{Colors.RESET}"


def get_color_by_name(color_name: str) -> str:
    """
    Get color code by name.

    Args:
        color_name: Name of the color (e.g., 'red', 'bright_green', 'bold')

    Returns:
        Color code string

    Raises:
        ValueError: If color name is not recognized
    """
    color_map = {
        # Standard colors
        "black": Colors.BLACK,
        "red": Colors.RED,
        "green": Colors.GREEN,
        "yellow": Colors.YELLOW,
        "blue": Colors.BLUE,
        "magenta": Colors.MAGENTA,
        "cyan": Colors.CYAN,
        "white": Colors.WHITE,
        # Bright colors
        "bright_black": Colors.BRIGHT_BLACK,
        "bright_red": Colors.BRIGHT_RED,
        "bright_green": Colors.BRIGHT_GREEN,
        "bright_yellow": Colors.BRIGHT_YELLOW,
        "bright_blue": Colors.BRIGHT_BLUE,
        "bright_magenta": Colors.BRIGHT_MAGENTA,
        "bright_cyan": Colors.BRIGHT_CYAN,
        "bright_white": Colors.BRIGHT_WHITE,
        # Formatting
        "bold": Colors.BOLD,
        "underline": Colors.UNDERLINE,
    }

    color_name = color_name.lower()
    if color_name not in color_map:
        raise ValueError(
            f"Unknown color: {color_name}. Available colors: {list(color_map.keys())}"
        )

    return color_map[color_name]
