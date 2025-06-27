#!/usr/bin/env python3
"""
Icon Inspector: A sandbox script to inspect all icons and see their visual spacing.
This helps identify which icons take up more space than others in terminal output.
"""

from jgmd2.logging import Logger, Colors, Icons, LogLevels


def inspect_all_icons():
    """Print all icons with sample text to inspect their visual spacing."""

    logger = Logger(
        name="icon_inspector",
        log_level=LogLevels.INFO,
        colored_console=True,
    )

    logger.print_header("Icon Spacing Inspector", color=Colors.BRIGHT_CYAN)

    # Group icons by category for better organization
    icon_categories = {
        "Success/Completion": ["SUCCESS", "COMPLETE", "DONE", "CHECK"],
        "Information": ["INFO", "NOTE", "BULB", "BOOK"],
        "Warning": ["WARNING", "ALERT", "BELL"],
        "Error/Failure": ["ERROR", "FAIL", "BUG", "CRASH"],
        "Processing/Progress": ["LOADING", "SPINNER", "GEAR", "ROCKET"],
        "Data/Storage": ["DATABASE", "FILE", "FOLDER", "DISK", "TABLE"],
        "Network/Communication": ["NETWORK", "WIFI", "EMAIL", "PHONE"],
        "Time": ["CLOCK", "TIMER", "CALENDAR"],
        "User/Action": ["USER", "TEAM", "HAND", "THUMBS_UP", "THUMBS_DOWN"],
        "Development": ["CODE", "TERMINAL", "DEBUG", "TEST"],
        "Business": ["MONEY", "CHART", "GRAPH", "TARGET"],
        "Fun/Misc": ["PARTY", "GIFT", "STAR", "HEART", "FIRE", "COOL"],
    }

    for category, icon_names in icon_categories.items():
        logger.info(lambda: f"\n--- {category} ---")

        for icon_name in icon_names:
            try:
                icon_value = Icons[icon_name].value
                logger.info(
                    lambda: f"{icon_value} {icon_name.lower()} - This is sample text to check spacing"
                )
            except KeyError:
                logger.error(lambda: f"[MISSING] {icon_name} - Icon not found in enum")

    logger.info(lambda: "\n" + "=" * 60)
    logger.info(
        lambda: "Icon inspection complete! Look for icons that appear to take up more or less space."
    )
    logger.info(
        lambda: "Some icons may appear wider due to emoji rendering differences."
    )


def inspect_icon_widths():
    """Print icons with a visual width indicator."""

    logger = Logger(
        name="icon_width_inspector",
        log_level=LogLevels.INFO,
        colored_console=True,
    )

    logger.print_header("Icon Width Analysis", color=Colors.BRIGHT_MAGENTA)

    # Create a visual grid to compare widths
    logger.info(lambda: "Icon width comparison (using dots as reference):")
    logger.info(lambda: "• = 1 character width")
    logger.info(lambda: "")

    # Test with a few key icons that might have width issues
    test_icons = [
        "SUCCESS",
        "INFO",
        "WARNING",
        "ERROR",
        "BUG",
        "LOADING",
        "DATABASE",
        "NETWORK",
        "USER",
        "CODE",
    ]

    for icon_name in test_icons:
        try:
            icon_value = Icons[icon_name].value
            logger.info(lambda: f"{icon_value} {icon_name}")
        except KeyError:
            logger.error(lambda: f"[MISSING] {icon_name}")


if __name__ == "__main__":
    print("🔍 Icon Inspector - Checking visual spacing of all icons")
    print("=" * 60)

    inspect_all_icons()
    print("\n")
    inspect_icon_widths()
