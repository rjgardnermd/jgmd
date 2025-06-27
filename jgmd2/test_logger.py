import unittest
import logging
import os
import tempfile
from unittest.mock import patch, MagicMock
from jgmd2 import Logger, LazyLogger, TableLogger


class TestLogger(unittest.TestCase):
    def setUp(self):
        self.tempfile = tempfile.NamedTemporaryFile(delete=False)
        self.log_file = self.tempfile.name
        self.logger = Logger(
            name="testlogger", log_file=self.log_file, log_level=logging.DEBUG
        )

    def tearDown(self):
        self.logger.close()
        self.tempfile.close()
        if os.path.exists(self.log_file):
            os.remove(self.log_file)

    def test_immediate_logging_levels(self):
        # Patch the logger to capture output
        with patch.object(self.logger.logger, "log") as mock_log:
            self.logger.debug(lambda: "debug message")
            self.logger.info(lambda: "info message")
            self.logger.warning(lambda: "warning message")
            self.logger.error(lambda: "error message")
            self.logger.critical(lambda: "critical message")
            self.logger.success(lambda: "success message")
            self.assertEqual(mock_log.call_count, 6)
            calls = [call[0][0] for call in mock_log.call_args_list]
            self.assertIn(logging.DEBUG, calls)
            self.assertIn(logging.INFO, calls)
            self.assertIn(logging.WARNING, calls)
            self.assertIn(logging.ERROR, calls)
            self.assertIn(logging.CRITICAL, calls)
            self.assertIn(25, calls)  # SUCCESS level

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

    def test_success_log_level(self):
        self.logger.success(lambda: "successful!")
        with open(self.log_file, "r") as f:
            content = f.read()
        self.assertIn("successful!", content)
        self.assertIn("SUCCESS", content)


class TestLazyLogger(unittest.TestCase):
    def setUp(self):
        self.tempfile = tempfile.NamedTemporaryFile(delete=False)
        self.log_file = self.tempfile.name
        self.logger = LazyLogger(
            name="testlazylogger", log_file=self.log_file, log_level=logging.DEBUG
        )

    def tearDown(self):
        self.logger.close()
        self.tempfile.close()
        if os.path.exists(self.log_file):
            os.remove(self.log_file)

    def test_lazy_logging(self):
        called = []
        self.logger.lazy_debug(lambda: called.append("debug") or "debug message")
        self.logger.lazy_info(lambda: called.append("info") or "info message")
        self.logger.lazy_warning(lambda: called.append("warning") or "warning message")
        self.logger.lazy_error(lambda: called.append("error") or "error message")
        self.logger.lazy_critical(
            lambda: called.append("critical") or "critical message"
        )
        self.logger.lazy_success(lambda: called.append("success") or "success message")
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


class TestTableLogger(unittest.TestCase):
    def setUp(self):
        self.tempfile = tempfile.NamedTemporaryFile(delete=False)
        self.log_file = self.tempfile.name
        self.headers = ["col1", "col2"]
        self.logger = TableLogger(
            self.headers,
            name="testtablelogger",
            log_file=self.log_file,
            log_level=logging.INFO,
        )

    def tearDown(self):
        self.logger.close()
        self.tempfile.close()
        if os.path.exists(self.log_file):
            os.remove(self.log_file)

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


if __name__ == "__main__":
    unittest.main()
