#!/usr/bin/env python3
"""
Sandbox script to demonstrate all features of the jgmd2 logging framework.
Run this script to see how Logger, LazyLogger, and TableLogger work.
"""

import time
import random
from jgmd2 import Logger, LazyLogger, TableLogger


def expensive_operation():
    """Simulate an expensive operation that we want to defer."""
    time.sleep(0.1)  # Simulate work
    return f"expensive_result_{random.randint(1, 1000)}"


def demo_immediate_logging():
    """Demonstrate immediate logging with Logger."""
    print("\n" + "=" * 60)
    print("DEMO: Immediate Logging (Logger)")
    print("=" * 60)

    logger = Logger(
        name="immediate_demo",
        log_file="immediate_demo.log",
        log_level="DEBUG",
        colored_console=True,
    )

    print("Logging messages immediately...")

    # All log levels
    logger.debug(lambda: f"Debug: {expensive_operation()}")
    logger.info(lambda: f"Info: Application started at {time.strftime('%H:%M:%S')}")
    logger.warning(lambda: f"Warning: High memory usage detected")
    logger.error(lambda: f"Error: Failed to connect to database")
    logger.critical(lambda: f"Critical: System shutdown required")
    logger.success(lambda: f"Success: Operation completed successfully!")

    print("✓ All messages logged immediately to console and file")
    print("Check 'immediate_demo.log' for file output")

    logger.close()


def demo_lazy_logging():
    """Demonstrate lazy/buffered logging with LazyLogger."""
    print("\n" + "=" * 60)
    print("DEMO: Lazy/Buffered Logging (LazyLogger)")
    print("=" * 60)

    logger = LazyLogger(
        name="lazy_demo",
        log_file="lazy_demo.log",
        log_level="DEBUG",
        colored_console=True,
    )

    print("Buffering messages (not logged yet)...")

    # Buffer messages without logging them
    logger.lazy_debug(lambda: f"Lazy Debug: {expensive_operation()}")
    logger.lazy_info(lambda: f"Lazy Info: Processing batch {random.randint(1, 100)}")
    logger.lazy_warning(lambda: f"Lazy Warning: Performance degradation detected")
    logger.lazy_error(lambda: f"Lazy Error: Network timeout")
    logger.lazy_critical(lambda: f"Lazy Critical: Data corruption detected")
    logger.lazy_success(lambda: f"Lazy Success: Batch processing completed!")

    print("✓ Messages buffered (not logged yet)")
    print("Flushing buffered messages...")

    # Now flush all buffered messages
    logger.flush_lazy()

    print("✓ All buffered messages now logged to console and file")
    print("Check 'lazy_demo.log' for file output")

    logger.close()


def demo_table_logging():
    """Demonstrate table logging with TableLogger."""
    print("\n" + "=" * 60)
    print("DEMO: Table Logging (TableLogger)")
    print("=" * 60)

    # Define table headers
    headers = ["User ID", "Name", "Status", "Last Login"]

    logger = TableLogger(
        headers=headers,
        name="table_demo",
        log_file="table_demo.log",
        log_level="INFO",
        colored_console=True,
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
    print("Check 'table_demo.log' for file output")

    logger.close()


def demo_deferred_evaluation():
    """Demonstrate the power of deferred evaluation."""
    print("\n" + "=" * 60)
    print("DEMO: Deferred Evaluation Benefits")
    print("=" * 60)

    logger = Logger(name="deferred_demo", log_level="INFO", colored_console=True)

    print("With deferred evaluation (lambda):")
    print("  - Expensive operations only run if log level is enabled")
    print("  - Variables are captured at lambda creation time")

    # This expensive operation won't run because log level is INFO
    logger.debug(lambda: f"DEBUG: {expensive_operation()}")
    print("✓ Debug message with expensive operation was NOT evaluated")

    # This expensive operation WILL run because log level is INFO
    logger.info(lambda: f"INFO: {expensive_operation()}")
    print("✓ Info message with expensive operation WAS evaluated")

    # Demonstrate variable capture
    user_id = "12345"
    logger.info(lambda: f"Processing user {user_id}")

    user_id = "67890"  # Change the variable
    logger.info(lambda: f"Processing user {user_id}")

    print("✓ Variables captured at lambda creation time")

    logger.close()


def demo_file_rotation():
    """Demonstrate file rotation capabilities."""
    print("\n" + "=" * 60)
    print("DEMO: File Rotation")
    print("=" * 60)

    logger = Logger(
        name="rotation_demo",
        log_file="rotation_demo.log",
        log_level="DEBUG",
        max_bytes=1024,  # Small size to trigger rotation quickly
        backup_count=3,
        colored_console=True,
    )

    print("Writing many log messages to trigger file rotation...")

    # Write enough messages to trigger rotation
    for i in range(50):
        logger.info(
            lambda: f"Message {i}: " + "x" * 50
        )  # Long message to fill file quickly

    print("✓ File rotation should have occurred")
    print("Check for rotation_demo.log, rotation_demo.log.1, etc.")

    logger.close()


def main():
    """Run all demos."""
    print("🎯 jgmd2 Logging Framework - Feature Demo")
    print("This script demonstrates all features of the logging framework.")

    try:
        # Run all demos
        demo_immediate_logging()
        demo_lazy_logging()
        demo_table_logging()
        demo_deferred_evaluation()
        demo_file_rotation()

        print("\n" + "=" * 60)
        print("🎉 ALL DEMOS COMPLETED!")
        print("=" * 60)
        print("Generated log files:")
        print("  - immediate_demo.log")
        print("  - lazy_demo.log")
        print("  - table_demo.log")
        print("  - rotation_demo.log (and rotated backups)")
        print("\nFeel free to examine these files to see the output!")

    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user.")
    except Exception as e:
        print(f"\nError during demo: {e}")


if __name__ == "__main__":
    main()
