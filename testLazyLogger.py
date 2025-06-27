#!/usr/bin/env python3
"""
Test script to demonstrate the LazyLogger sync_mode functionality.
"""

from jgmd2.logging.core.lazy_logger import LazyLogger
import time


def expensive_operation():
    """Simulate an expensive operation for testing lazy logging."""
    time.sleep(0.1)  # Simulate some work
    return "Expensive operation completed"


def test_lazy_logger():
    print("=== Testing LazyLogger with sync_mode=False (default) ===")

    # Normal lazy logger (buffers messages)
    logger = LazyLogger("test_lazy", sync_mode=False)

    print("Adding lazy log messages (they will be buffered)...")
    logger.lazy_debug(lambda: "This is a lazy debug message")
    logger.lazy_info(lambda: "This is a lazy info message")
    logger.lazy_warning(lambda: f"Warning: {expensive_operation()}")
    logger.lazy_error(lambda: "This is a lazy error message")
    logger.lazy_critical(lambda: "This is a lazy critical message")

    print("Messages are buffered, not logged yet.")
    print("Now flushing...")
    logger.flush_lazy()

    print("\n" + "=" * 60 + "\n")

    print("=== Testing LazyLogger with sync_mode=True ===")

    # Sync mode logger (logs immediately)
    sync_logger = LazyLogger("test_sync", sync_mode=True)

    print("Adding lazy log messages (they will be logged immediately)...")
    sync_logger.lazy_debug(lambda: "This is a sync debug message")
    sync_logger.lazy_info(lambda: "This is a sync info message")
    sync_logger.lazy_warning(lambda: f"Sync warning: {expensive_operation()}")
    sync_logger.lazy_error(lambda: "This is a sync error message")
    sync_logger.lazy_critical(lambda: "This is a sync critical message")

    print("Messages were logged immediately due to sync_mode=True")
    print("No flush needed in sync mode.")


if __name__ == "__main__":
    test_lazy_logger()
