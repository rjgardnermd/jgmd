import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime
import traceback

from jgmd2.util.errorUtil import exception_to_str, get_error_handling_decorators


class TestErrorUtil:
    """Test cases for errorUtil module."""

    def test_exception_to_str_basic(self):
        """Test basic exception to string conversion."""
        try:
            raise ValueError("Test error message")
        except ValueError as e:
            result = exception_to_str(e)

            assert isinstance(result, str)
            assert "Exception was thrown at" in result
            assert "ValueError: Test error message" in result
            assert "Traceback" in result

    def test_exception_to_str_with_complex_exception(self):
        """Test exception to string conversion with a complex exception."""

        def nested_function():
            def inner_function():
                raise RuntimeError("Inner error")

            inner_function()

        try:
            nested_function()
        except RuntimeError as e:
            result = exception_to_str(e)

            assert isinstance(result, str)
            assert "Exception was thrown at" in result
            assert "RuntimeError: Inner error" in result
            assert "Traceback" in result
            assert "nested_function" in result
            assert "inner_function" in result

    def test_exception_to_str_timestamp_format(self):
        """Test that the timestamp in exception string is properly formatted."""
        try:
            raise Exception("Test")
        except Exception as e:
            result = exception_to_str(e)

            # Check timestamp format (YYYY-MM-DD HH:MM:SS)
            lines = result.split("\n")
            timestamp_line = lines[0]
            assert "Exception was thrown at" in timestamp_line

            # Extract timestamp part - it should be in format "YYYY-MM-DD HH:MM:SS"
            timestamp_part = timestamp_line.split("Exception was thrown at ")[1].split(
                ":"
            )[0]
            # The timestamp part should be "YYYY-MM-DD HH" (13 chars) before the first colon
            assert len(timestamp_part) == 13  # YYYY-MM-DD HH
            assert timestamp_part.count("-") == 2
            assert timestamp_part.count(" ") == 1

    def test_get_error_handling_decorators_returns_tuple(self):
        """Test that get_error_handling_decorators returns a tuple of two callables."""

        def mock_error_handler(error_msg: str):
            pass

        handle_error, handle_error_async = get_error_handling_decorators(
            mock_error_handler
        )

        assert callable(handle_error)
        assert callable(handle_error_async)

    def test_handle_error_decorator_success(self):
        """Test handle_error decorator when function succeeds."""
        error_calls = []

        def mock_error_handler(error_msg: str):
            error_calls.append(error_msg)

        handle_error, _ = get_error_handling_decorators(mock_error_handler)

        @handle_error
        def successful_function():
            return "success"

        result = successful_function()

        assert result == "success"
        assert len(error_calls) == 0

    def test_handle_error_decorator_exception(self):
        """Test handle_error decorator when function raises an exception."""
        error_calls = []

        def mock_error_handler(error_msg: str):
            error_calls.append(error_msg)

        handle_error, _ = get_error_handling_decorators(mock_error_handler)

        @handle_error
        def failing_function():
            raise ValueError("Test error")

        failing_function()  # Should not raise exception

        assert len(error_calls) == 1
        assert "Exception was thrown at" in error_calls[0]
        assert "ValueError: Test error" in error_calls[0]

    def test_handle_error_decorator_with_arguments(self):
        """Test handle_error decorator with function arguments."""
        error_calls = []

        def mock_error_handler(error_msg: str):
            error_calls.append(error_msg)

        handle_error, _ = get_error_handling_decorators(mock_error_handler)

        @handle_error
        def function_with_args(a, b, c=None):
            if a == 0:
                raise ValueError(f"Invalid value: {a}")
            return a + b + (c or 0)

        # Test successful call
        result = function_with_args(1, 2, 3)
        assert result == 6
        assert len(error_calls) == 0

        # Test failing call
        function_with_args(0, 2, 3)
        assert len(error_calls) == 1
        assert "ValueError: Invalid value: 0" in error_calls[0]

    def test_handle_error_decorator_with_kwargs(self):
        """Test handle_error decorator with keyword arguments."""
        error_calls = []

        def mock_error_handler(error_msg: str):
            error_calls.append(error_msg)

        handle_error, _ = get_error_handling_decorators(mock_error_handler)

        @handle_error
        def function_with_kwargs(**kwargs):
            if "fail" in kwargs:
                raise RuntimeError("Keyword triggered error")
            return kwargs

        # Test successful call
        result = function_with_kwargs(a=1, b=2)
        assert result == {"a": 1, "b": 2}
        assert len(error_calls) == 0

        # Test failing call
        function_with_kwargs(fail=True)
        assert len(error_calls) == 1
        assert "RuntimeError: Keyword triggered error" in error_calls[0]

    @pytest.mark.asyncio
    async def test_handle_error_async_decorator_success(self):
        """Test handle_error_async decorator when async function succeeds."""
        error_calls = []

        def mock_error_handler(error_msg: str):
            error_calls.append(error_msg)

        _, handle_error_async = get_error_handling_decorators(mock_error_handler)

        @handle_error_async
        async def successful_async_function():
            return "async success"

        result = await successful_async_function()

        assert result == "async success"
        assert len(error_calls) == 0

    @pytest.mark.asyncio
    async def test_handle_error_async_decorator_exception(self):
        """Test handle_error_async decorator when async function raises an exception."""
        error_calls = []

        def mock_error_handler(error_msg: str):
            error_calls.append(error_msg)

        _, handle_error_async = get_error_handling_decorators(mock_error_handler)

        @handle_error_async
        async def failing_async_function():
            raise RuntimeError("Async test error")

        await failing_async_function()  # Should not raise exception

        assert len(error_calls) == 1
        assert "Exception was thrown at" in error_calls[0]
        assert "RuntimeError: Async test error" in error_calls[0]

    @pytest.mark.asyncio
    async def test_handle_error_async_decorator_with_arguments(self):
        """Test handle_error_async decorator with function arguments."""
        error_calls = []

        def mock_error_handler(error_msg: str):
            error_calls.append(error_msg)

        _, handle_error_async = get_error_handling_decorators(mock_error_handler)

        @handle_error_async
        async def async_function_with_args(a, b, c=None):
            if a < 0:
                raise ValueError(f"Negative value: {a}")
            return a + b + (c or 0)

        # Test successful call
        result = await async_function_with_args(1, 2, 3)
        assert result == 6
        assert len(error_calls) == 0

        # Test failing call
        await async_function_with_args(-1, 2, 3)
        assert len(error_calls) == 1
        assert "ValueError: Negative value: -1" in error_calls[0]

    def test_error_handler_called_with_proper_format(self):
        """Test that error handler is called with properly formatted error message."""
        error_calls = []

        def mock_error_handler(error_msg: str):
            error_calls.append(error_msg)

        handle_error, _ = get_error_handling_decorators(mock_error_handler)

        @handle_error
        def test_function():
            raise TypeError("Type error test")

        test_function()

        assert len(error_calls) == 1
        error_msg = error_calls[0]

        # Check format
        lines = error_msg.split("\n")
        assert len(lines) >= 3  # Timestamp line + traceback lines

        # Check timestamp line
        assert lines[0].startswith("Exception was thrown at")

        # Check traceback contains the error
        traceback_text = "\n".join(lines[1:])
        assert "TypeError: Type error test" in traceback_text
        assert "test_function" in traceback_text

    def test_multiple_exceptions_handled_separately(self):
        """Test that multiple exceptions are handled separately."""
        error_calls = []

        def mock_error_handler(error_msg: str):
            error_calls.append(error_msg)

        handle_error, _ = get_error_handling_decorators(mock_error_handler)

        @handle_error
        def function1():
            raise ValueError("Error 1")

        @handle_error
        def function2():
            raise RuntimeError("Error 2")

        function1()
        function2()

        assert len(error_calls) == 2
        assert "ValueError: Error 1" in error_calls[0]
        assert "RuntimeError: Error 2" in error_calls[1]
