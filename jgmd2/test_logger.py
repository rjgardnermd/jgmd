import unittest
import logging
import os
import tempfile
from unittest.mock import patch, MagicMock
from jgmd2 import Logger, LazyLogger, TableLogger
from jgmd2.colors import Colors
from jgmd2.icons import Icons


class TestLogger(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.log_file = os.path.join(self.tempdir.name, "testlogger.log")
        self.logger = Logger(
            name="testlogger",
            log_directory=self.tempdir.name,
            file_name="testlogger.log",
            log_level=logging.DEBUG,
        )

    def tearDown(self):
        self.logger.close()
        self.tempdir.cleanup()

    def test_immediate_logging_levels(self):
        # Patch the logger to capture output
        with patch.object(self.logger.logger, "handle") as mock_handle:
            self.logger.debug(lambda: "debug message")
            self.logger.info(lambda: "info message")
            self.logger.warning(lambda: "warning message")
            self.logger.error(lambda: "error message")
            self.logger.critical(lambda: "critical message")
            self.logger.info(lambda: "success message", color=Colors.GREEN)
            self.assertEqual(mock_handle.call_count, 6)
            levels = [call[0][0].levelno for call in mock_handle.call_args_list]
            self.assertIn(logging.DEBUG, levels)
            self.assertIn(logging.INFO, levels)
            self.assertIn(logging.WARNING, levels)
            self.assertIn(logging.ERROR, levels)
            self.assertIn(logging.CRITICAL, levels)

    def test_deferred_evaluation(self):
        called = []

        def expensive():
            called.append(True)
            return "expensive"

        self.logger.info(lambda: expensive())
        self.assertTrue(called)

    def test_file_logging(self):
        self.logger.info(lambda: "file test message")
        with open(self.log_file, "r") as f:
            content = f.read()
        self.assertIn("file test message", content)

    def test_success_log_color(self):
        self.logger.info(lambda: "successful!", color=Colors.GREEN)
        with open(self.log_file, "r") as f:
            content = f.read()
        self.assertIn("successful!", content)
        self.assertIn("INFO", content)

    def test_icons_in_logging(self):
        self.logger.info(lambda: f"{Icons.SUCCESS.value} Operation completed")
        with open(self.log_file, "r") as f:
            content = f.read()
        self.assertIn("✅", content)
        self.assertIn("Operation completed", content)

    def test_colors_enum(self):
        # Test that Colors enum values are strings
        self.assertIsInstance(Colors.RED.value, str)
        self.assertIsInstance(Colors.GREEN.value, str)
        self.assertIsInstance(Colors.BLUE.value, str)

        # Test colorize method
        colored_text = Colors.colorize("test", Colors.RED)
        self.assertIn(Colors.RED.value, colored_text)
        self.assertIn(Colors.RESET.value, colored_text)

    def test_icons_enum(self):
        # Test that Icons enum values are strings
        self.assertIsInstance(Icons.SUCCESS.value, str)
        self.assertIsInstance(Icons.ERROR.value, str)
        self.assertIsInstance(Icons.INFO.value, str)


class TestLazyLogger(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.log_file = os.path.join(self.tempdir.name, "testlazylogger.log")
        self.logger = LazyLogger(
            name="testlazylogger",
            log_directory=self.tempdir.name,
            file_name="testlazylogger.log",
            log_level=logging.DEBUG,
        )

    def tearDown(self):
        self.logger.close()
        self.tempdir.cleanup()

    def test_lazy_logging(self):
        called = []
        self.logger.lazy_debug(lambda: called.append("debug") or "debug message")
        self.logger.lazy_info(lambda: called.append("info") or "info message")
        self.logger.lazy_warning(lambda: called.append("warning") or "warning message")
        self.logger.lazy_error(lambda: called.append("error") or "error message")
        self.logger.lazy_critical(
            lambda: called.append("critical") or "critical message"
        )
        self.logger.lazy_info(
            lambda: called.append("success") or "success message", color=Colors.GREEN
        )
        # Nothing should be called yet
        self.assertEqual(called, [])
        self.logger.flush_lazy()
        # All should be called after flush
        self.assertEqual(
            set(called), {"debug", "info", "warning", "error", "critical", "success"}
        )
        with open(self.log_file, "r") as f:
            content = f.read()
        self.assertIn("debug message", content)
        self.assertIn("info message", content)
        self.assertIn("warning message", content)
        self.assertIn("error message", content)
        self.assertIn("critical message", content)
        self.assertIn("success message", content)

    def test_clear_lazy(self):
        self.logger.lazy_info(lambda: "should not log")
        self.logger.clear_lazy()
        self.logger.flush_lazy()
        with open(self.log_file, "r") as f:
            content = f.read()
        self.assertNotIn("should not log", content)

    def test_lazy_icons_and_colors(self):
        self.logger.lazy_info(
            lambda: f"{Icons.ROCKET.value} Launching...", color=Colors.BRIGHT_GREEN
        )
        self.logger.flush_lazy()
        with open(self.log_file, "r") as f:
            content = f.read()
        self.assertIn("🚀", content)
        self.assertIn("Launching...", content)


class TestTableLogger(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.log_file = os.path.join(self.tempdir.name, "testtablelogger.log")
        self.headers = ["col1", "col2"]
        self.logger = TableLogger(
            self.headers,
            name="testtablelogger",
            log_directory=self.tempdir.name,
            file_name="testtablelogger.log",
            log_level=logging.INFO,
        )

    def tearDown(self):
        self.logger.close()
        self.tempdir.cleanup()

    def test_log_row(self):
        self.logger.log_row(lambda: [1, 2])
        with open(self.log_file, "r") as f:
            content = f.read()
        self.assertIn("col1", content)
        self.assertIn("1", content)
        self.assertIn("2", content)

    def test_log_table(self):
        self.logger.log_table(lambda: [[1, 2], [3, 4]])
        with open(self.log_file, "r") as f:
            content = f.read()
        self.assertIn("col1", content)
        self.assertIn("3", content)
        self.assertIn("4", content)

    def test_lazy_log_row_and_table(self):
        self.logger.lazy_log_row(lambda: [5, 6])
        self.logger.lazy_log_table(lambda: [[7, 8], [9, 10]])
        self.logger.flush_lazy()
        with open(self.log_file, "r") as f:
            content = f.read()
        self.assertIn("5", content)
        self.assertIn("6", content)
        self.assertIn("7", content)
        self.assertIn("8", content)
        self.assertIn("9", content)
        self.assertIn("10", content)

    def test_table_with_icons_and_colors(self):
        self.logger.log_row(
            lambda: [f"{Icons.USER.value} Alice", "Active"], color=Colors.GREEN
        )
        with open(self.log_file, "r") as f:
            content = f.read()
        self.assertIn("👤", content)
        self.assertIn("Alice", content)
        self.assertIn("Active", content)


if __name__ == "__main__":
    unittest.main()
