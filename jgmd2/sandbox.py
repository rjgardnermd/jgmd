#!/usr/bin/env python3
"""
Sandbox script to demonstrate all features of the jgmd2 logging framework.
Run this script to see how Logger, LazyLogger, and TableLogger work.
"""

import time
import random
import os
from jgmd2 import Logger, LazyLogger, TableLogger
from jgmd2.colors import Colors
from jgmd2.icons import Icons


def expensive_operation():
    """Simulate an expensive operation that we want to defer."""
    time.sleep(0.1)  # Simulate work
    return f"expensive_result_{random.randint(1, 1000)}"


def demo_immediate_logging():
    """Demonstrate immediate logging with Logger."""
    logger = Logger(
        name="immediate_demo",
        log_directory="logs",
        file_name="immediate_demo.log",
        log_level="DEBUG",
        colored_console=True,
    )

    logger.print_header(
        f"{Icons.COMPLETE.value} DEMO: Immediate Logging (Logger)",
        color=Colors.BRIGHT_GREEN,
    )

    print("Logging messages immediately...")

    # All log levels with icons and colors
    logger.debug(lambda: f"{Icons.DEBUG.value} Debug: {expensive_operation()}")
    logger.info(
        lambda: f"{Icons.INFO.value} Info: Application started at {time.strftime('%H:%M:%S')}"
    )
    logger.warning(lambda: f"{Icons.WARNING.value} Warning: High memory usage detected")
    logger.error(lambda: f"{Icons.ERROR.value} Error: Failed to connect to database")
    logger.critical(lambda: f"{Icons.CRASH.value} Critical: System shutdown required")
    logger.info(
        lambda: f"{Icons.SUCCESS.value} Success: Operation completed successfully!",
        color=Colors.GREEN,
    )

    print("✓ All messages logged immediately to console and file")
    print("Check 'logs/immediate_demo.log' for file output")

    logger.close()


def demo_lazy_logging():
    """Demonstrate lazy/buffered logging with LazyLogger."""
    logger = LazyLogger(
        name="lazy_demo",
        log_directory="logs",
        file_name="lazy_demo.log",
        log_level="DEBUG",
        colored_console=True,
    )

    logger.lazy_print_header(
        f"{Icons.LOADING.value} DEMO: Lazy/Buffered Logging (LazyLogger)",
        color=Colors.BRIGHT_BLUE,
    )

    print("Buffering messages (not logged yet)...")

    # Buffer messages without logging them
    logger.lazy_debug(
        lambda: f"{Icons.DEBUG.value} Lazy Debug: {expensive_operation()}"
    )
    logger.lazy_info(
        lambda: f"{Icons.INFO.value} Lazy Info: Processing batch {random.randint(1, 100)}"
    )
    logger.lazy_warning(
        lambda: f"{Icons.WARNING.value} Lazy Warning: Performance degradation detected"
    )
    logger.lazy_error(lambda: f"{Icons.ERROR.value} Lazy Error: Network timeout")
    logger.lazy_critical(
        lambda: f"{Icons.CRASH.value} Lazy Critical: Data corruption detected"
    )
    logger.lazy_info(
        lambda: f"{Icons.SUCCESS.value} Lazy Success: Batch processing completed!",
        color=Colors.GREEN,
    )

    print("✓ Messages buffered (not logged yet)")
    print("Flushing buffered messages...")

    # Now flush all buffered messages
    logger.flush_lazy()

    print("✓ All buffered messages now logged to console and file")
    print("Check 'logs/lazy_demo.log' for file output")

    logger.close()


def demo_table_logging():
    """Demonstrate table logging with TableLogger."""
    # Define table headers
    headers = ["User ID", "Name", "Status", "Last Login"]

    logger = TableLogger(
        headers=headers,
        name="table_demo",
        log_directory="logs",
        file_name="table_demo.log",
        log_level="INFO",
        colored_console=True,
    )

    logger.print_header(
        f"{Icons.TABLE.value} DEMO: Table Logging (TableLogger)",
        color=Colors.BRIGHT_MAGENTA,
    )

    print("Logging individual rows...")

    # Log individual rows
    logger.log_row(lambda: ["001", "Alice", "Active", "2024-01-15 10:30:00"])
    logger.log_row(lambda: ["002", "Bob", "Inactive", "2024-01-10 14:20:00"])

    print("Logging complete table...")

    # Log a complete table
    logger.log_table(
        lambda: [
            ["003", "Charlie", "Active", "2024-01-16 09:15:00"],
            ["004", "Diana", "Active", "2024-01-16 11:45:00"],
            ["005", "Eve", "Inactive", "2024-01-12 16:30:00"],
        ]
    )

    print("Lazy table logging...")

    # Lazy table logging
    logger.lazy_log_row(lambda: ["006", "Frank", "Active", "2024-01-16 13:20:00"])
    logger.lazy_log_table(
        lambda: [
            ["007", "Grace", "Active", "2024-01-16 15:10:00"],
            ["008", "Henry", "Inactive", "2024-01-11 12:00:00"],
        ]
    )

    print("Flushing lazy table logs...")
    logger.flush_lazy()

    print("✓ All table data logged to console and file")
    print("Check 'logs/table_demo.log' for file output")

    logger.close()


def demo_deferred_evaluation():
    """Demonstrate the power of deferred evaluation."""
    logger = Logger(name="deferred_demo", log_level="INFO", colored_console=True)

    logger.print_header(
        f"{Icons.BULB.value} DEMO: Deferred Evaluation Benefits",
        color=Colors.BRIGHT_CYAN,
    )

    print("With deferred evaluation (lambda):")
    print("  - Expensive operations only run if log level is enabled")
    print("  - Variables are captured at lambda creation time")

    # This expensive operation won't run because log level is INFO
    logger.debug(lambda: f"{Icons.DEBUG.value} DEBUG: {expensive_operation()}")
    print("✓ Debug message with expensive operation was NOT evaluated")

    # This expensive operation WILL run because log level is INFO
    logger.info(lambda: f"{Icons.INFO.value} INFO: {expensive_operation()}")
    print("✓ Info message with expensive operation WAS evaluated")

    # Demonstrate variable capture
    user_id = "12345"
    logger.info(lambda: f"{Icons.USER.value} Processing user {user_id}")

    user_id = "67890"  # Change the variable
    logger.info(lambda: f"{Icons.USER.value} Processing user {user_id}")

    print("✓ Variables captured at lambda creation time")

    logger.close()


def demo_file_rotation():
    """Demonstrate file rotation capabilities."""
    logger = Logger(
        name="rotation_demo",
        log_directory="logs",
        file_name="rotation_demo.log",
        log_level="DEBUG",
        max_bytes=1024,  # Small size to trigger rotation quickly
        backup_count=3,
        colored_console=True,
    )

    logger.print_header(
        f"{Icons.GEAR.value} DEMO: File Rotation", color=Colors.BRIGHT_YELLOW
    )

    print("Writing many log messages to trigger file rotation...")

    # Write enough messages to trigger rotation
    for i in range(50):
        logger.info(
            lambda: f"{Icons.FILE.value} Message {i}: " + "x" * 50
        )  # Long message to fill file quickly

    print("✓ File rotation should have occurred")
    print("Check for logs/rotation_demo.log, logs/rotation_demo.log.1, etc.")

    logger.close()


def demo_icons_and_colors():
    """Demonstrate the new icons and colors enums."""
    logger = Logger(name="icons_demo", log_level="INFO", colored_console=True)

    logger.print_header(
        f"{Icons.STAR.value} DEMO: Icons and Colors", color=Colors.BRIGHT_MAGENTA
    )

    # Demonstrate different icons with different colors
    logger.info(
        lambda: f"{Icons.ROCKET.value} Application launched successfully!",
        color=Colors.BRIGHT_GREEN,
    )
    logger.info(
        lambda: f"{Icons.DATABASE.value} Database connection established",
        color=Colors.BLUE,
    )
    logger.info(
        lambda: f"{Icons.NETWORK.value} Network request completed", color=Colors.CYAN
    )
    logger.info(
        lambda: f"{Icons.MONEY.value} Transaction processed", color=Colors.BRIGHT_YELLOW
    )
    logger.info(
        lambda: f"{Icons.HEART.value} User feedback received", color=Colors.BRIGHT_RED
    )
    logger.info(
        lambda: f"{Icons.COOL.value} All systems operational", color=Colors.BRIGHT_CYAN
    )

    logger.close()


def demo_cloud_logging_compatibility():
    """Demonstrate cloud logging compatibility with text alternatives."""
    logger = Logger(name="cloud_demo", log_level="INFO", colored_console=True)

    logger.print_header(
        f"{Icons.TARGET.value} DEMO: Cloud Logging Compatibility",
        color=Colors.BRIGHT_CYAN,
    )

    print("Emoji icons (default):")
    logger.info(lambda: f"{Icons.get_icon('SUCCESS')} Operation completed")
    logger.info(lambda: f"{Icons.get_icon('ERROR')} Something went wrong")
    logger.info(lambda: f"{Icons.get_icon('ROCKET')} Application launched")

    print("\nText alternatives (cloud-friendly):")
    logger.info(
        lambda: f"{Icons.get_icon('SUCCESS', use_icons=False)} Operation completed"
    )
    logger.info(
        lambda: f"{Icons.get_icon('ERROR', use_icons=False)} Something went wrong"
    )
    logger.info(
        lambda: f"{Icons.get_icon('ROCKET', use_icons=False)} Application launched"
    )

    print("\nEnvironment variable control:")
    print("Set JGMD_USE_ICONS=false to disable emojis globally")
    print("Set JGMD_USE_ICONS=true to enable emojis (default)")

    logger.close()


def main():
    """Run all demos."""
    print(f"{Icons.TARGET.value} jgmd2 Logging Framework - Feature Demo")
    print("This script demonstrates all features of the logging framework.")

    try:
        # Run all demos
        demo_immediate_logging()
        demo_lazy_logging()
        demo_table_logging()
        demo_deferred_evaluation()
        demo_file_rotation()
        demo_icons_and_colors()
        demo_cloud_logging_compatibility()

        print("\n" + "=" * 60)
        print(f"{Icons.PARTY.value} ALL DEMOS COMPLETED!")
        print("=" * 60)
        print("Generated log files:")
        print("  - immediate_demo.log")
        print("  - lazy_demo.log")
        print("  - table_demo.log")
        print("  - rotation_demo.log (and rotated backups)")
        print("\nFeel free to examine these files to see the output!")

    except KeyboardInterrupt:
        print(f"\n\n{Icons.HAND.value} Demo interrupted by user.")
    except Exception as e:
        print(f"\n{Icons.BUG.value} Error during demo: {e}")


if __name__ == "__main__":
    main()
