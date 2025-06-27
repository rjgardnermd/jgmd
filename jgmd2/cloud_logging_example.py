#!/usr/bin/env python3
"""
Example script showing how to use jgmd2 logging in cloud environments
where emoji icons might cause issues with log aggregation systems.
"""

import os
from jgmd2 import Logger, LazyLogger
from jgmd2.colors import Colors
from jgmd2.icons import Icons


def demo_cloud_compatible_logging():
    """Demonstrate logging that's compatible with cloud platforms like Splunk, ELK, Datadog."""

    # Option 1: Disable icons globally via environment variable
    os.environ["JGMD_USE_ICONS"] = "false"

    logger = Logger(
        name="cloud_app",
        log_directory="logs",
        file_name="cloud_app.log",
        log_level="INFO",
        colored_console=True,
    )

    logger.print_header("Cloud-Compatible Logging Demo", color=Colors.BLUE)

    # These will use text alternatives instead of emojis
    logger.info(lambda: f"{Icons.get_icon('SUCCESS')} User authentication successful")
    logger.info(lambda: f"{Icons.get_icon('DATABASE')} Database query executed")
    logger.warning(lambda: f"{Icons.get_icon('WARNING')} High memory usage detected")
    logger.error(lambda: f"{Icons.get_icon('ERROR')} API request failed")

    logger.close()


def demo_mixed_logging():
    """Demonstrate mixing emoji and text icons based on context."""

    # Re-enable icons for console output
    os.environ["JGMD_USE_ICONS"] = "true"

    logger = Logger(
        name="mixed_app",
        log_directory="logs",
        file_name="mixed_app.log",
        log_level="INFO",
        colored_console=True,
    )

    logger.print_header("Mixed Icon Usage Demo", color=Colors.BRIGHT_MAGENTA)

    # Use emojis for user-facing messages
    logger.info(
        lambda: f"{Icons.get_icon('ROCKET')} Application launched successfully!"
    )

    # Use text alternatives for technical/system messages that go to cloud logs
    logger.info(
        lambda: f"{Icons.get_icon('DATABASE', use_icons=False)} DB_CONNECTION_ESTABLISHED"
    )
    logger.info(
        lambda: f"{Icons.get_icon('NETWORK', use_icons=False)} API_ENDPOINT_CALLED"
    )
    logger.error(
        lambda: f"{Icons.get_icon('ERROR', use_icons=False)} EXCEPTION_THROWN: ConnectionTimeout"
    )

    logger.close()


def demo_lazy_cloud_logging():
    """Demonstrate lazy logging with cloud compatibility."""

    # Disable icons for this demo
    os.environ["JGMD_USE_ICONS"] = "false"

    logger = LazyLogger(
        name="lazy_cloud_app",
        log_directory="logs",
        file_name="lazy_cloud_app.log",
        log_level="INFO",
        colored_console=True,
    )

    logger.lazy_print_header("Lazy Cloud Logging Demo", color=Colors.BRIGHT_GREEN)

    # Buffer messages with text alternatives
    logger.lazy_info(lambda: f"{Icons.get_icon('LOADING')} Processing batch job")
    logger.lazy_info(lambda: f"{Icons.get_icon('GEAR')} Configuration loaded")
    logger.lazy_warning(
        lambda: f"{Icons.get_icon('ALERT')} Performance threshold exceeded"
    )
    logger.lazy_error(lambda: f"{Icons.get_icon('CRASH')} Critical system failure")

    # Flush all messages at once
    logger.flush_lazy()

    logger.close()


def main():
    """Run cloud logging examples."""
    print("🌐 jgmd2 Cloud Logging Compatibility Examples")
    print("=" * 50)

    print("\n1. Cloud-Compatible Logging (Text Icons)")
    demo_cloud_compatible_logging()

    print("\n2. Mixed Icon Usage")
    demo_mixed_logging()

    print("\n3. Lazy Cloud Logging")
    demo_lazy_cloud_logging()

    print("\n" + "=" * 50)
    print("Cloud Logging Best Practices:")
    print("• Use JGMD_USE_ICONS=false for production cloud environments")
    print("• Use text alternatives for technical/system logs")
    print("• Emojis are fine for user-facing console output")
    print("• Consider your log aggregation platform's Unicode support")
    print("• Test log parsing and search functionality with your platform")


if __name__ == "__main__":
    main()
