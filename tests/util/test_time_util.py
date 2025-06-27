import time
import pytest
from datetime import datetime, timezone, timedelta
from unittest.mock import patch, MagicMock

from jgmd2.util.timeUtil import (
    time_it,
    seconds_since_timestamp,
    seconds_since_datetime,
    subtract_seconds_from_datetime,
    datetime_to_str,
    timestamp_to_str,
    get_cutoff_date,
    datetimes_are_equal,
)


class TestTimeUtil:
    """Test cases for timeUtil module."""

    def test_time_it_decorator_success(self):
        """Test time_it decorator with successful function."""

        @time_it
        def test_function():
            time.sleep(0.01)  # Small delay to ensure measurable time
            return "success"

        # Capture stdout to check the timing output
        with patch("builtins.print") as mock_print:
            result = test_function()

        assert result == "success"
        mock_print.assert_called_once()
        call_args = mock_print.call_args[0][0]
        assert "function test_function took" in call_args
        assert "seconds" in call_args

    def test_time_it_decorator_with_arguments(self):
        """Test time_it decorator with function arguments."""

        @time_it
        def test_function(a, b, c=0):
            time.sleep(0.01)
            return a + b + c

        with patch("builtins.print") as mock_print:
            result = test_function(1, 2, 3)

        assert result == 6
        mock_print.assert_called_once()
        call_args = mock_print.call_args[0][0]
        assert "function test_function took" in call_args

    def test_time_it_decorator_with_kwargs(self):
        """Test time_it decorator with keyword arguments."""

        @time_it
        def test_function(**kwargs):
            time.sleep(0.01)
            return sum(kwargs.values())

        with patch("builtins.print") as mock_print:
            result = test_function(a=1, b=2, c=3)

        assert result == 6
        mock_print.assert_called_once()

    def test_seconds_since_timestamp(self):
        """Test seconds_since_timestamp function."""
        # Create a timestamp from 10 seconds ago
        past_timestamp = time.time() - 10

        result = seconds_since_timestamp(past_timestamp)

        # Should be approximately 10 seconds (allow small tolerance)
        assert 9.5 <= result <= 10.5

    def test_seconds_since_timestamp_future(self):
        """Test seconds_since_timestamp with future timestamp."""
        # Create a timestamp from 5 seconds in the future
        future_timestamp = time.time() + 5

        result = seconds_since_timestamp(future_timestamp)

        # Should be approximately -5 seconds (negative because it's in the future)
        assert -5.5 <= result <= -4.5

    def test_seconds_since_datetime_with_timezone(self):
        """Test seconds_since_datetime with timezone-aware datetime."""
        # Create a datetime from 10 seconds ago with UTC timezone
        past_datetime = datetime.now(timezone.utc) - timedelta(seconds=10)

        result = seconds_since_datetime(past_datetime)

        # Should be approximately 10 seconds
        assert 9.5 <= result <= 10.5

    def test_seconds_since_datetime_without_timezone(self):
        """Test seconds_since_datetime with timezone-naive datetime."""
        # Create a timezone-naive datetime from 10 seconds ago
        past_datetime = datetime.now() - timedelta(seconds=10)

        result = seconds_since_datetime(past_datetime)

        # Should be approximately 10 seconds
        assert 9.5 <= result <= 10.5

    def test_seconds_since_datetime_future(self):
        """Test seconds_since_datetime with future datetime."""
        # Create a datetime from 5 seconds in the future
        future_datetime = datetime.now() + timedelta(seconds=5)

        result = seconds_since_datetime(future_datetime)

        # Should be approximately -5 seconds
        assert -5.5 <= result <= -4.5

    def test_subtract_seconds_from_datetime(self):
        """Test subtract_seconds_from_datetime function."""
        # Create a base datetime
        base_datetime = datetime(2023, 1, 1, 12, 0, 0)

        # Subtract 3600 seconds (1 hour)
        result = subtract_seconds_from_datetime(base_datetime, 3600)

        expected = datetime(2023, 1, 1, 11, 0, 0)
        assert result == expected

    def test_subtract_seconds_from_datetime_with_timezone(self):
        """Test subtract_seconds_from_datetime with timezone-aware datetime."""
        # Create a timezone-aware datetime
        base_datetime = datetime(2023, 1, 1, 12, 0, 0, tzinfo=timezone.utc)

        # Subtract 1800 seconds (30 minutes)
        result = subtract_seconds_from_datetime(base_datetime, 1800)

        expected = datetime(2023, 1, 1, 11, 30, 0, tzinfo=timezone.utc)
        assert result == expected

    def test_subtract_seconds_from_datetime_zero_seconds(self):
        """Test subtract_seconds_from_datetime with zero seconds."""
        base_datetime = datetime(2023, 1, 1, 12, 0, 0)

        result = subtract_seconds_from_datetime(base_datetime, 0)

        assert result == base_datetime

    def test_datetime_to_str(self):
        """Test datetime_to_str function."""
        test_datetime = datetime(2023, 12, 25, 15, 30, 45)

        result = datetime_to_str(test_datetime)

        assert result == "2023-12-25 15:30:45"

    def test_datetime_to_str_with_timezone(self):
        """Test datetime_to_str with timezone-aware datetime."""
        test_datetime = datetime(2023, 12, 25, 15, 30, 45, tzinfo=timezone.utc)

        result = datetime_to_str(test_datetime)

        # Should still format correctly (timezone info is preserved but not shown in string)
        assert result == "2023-12-25 15:30:45"

    def test_timestamp_to_str(self):
        """Test timestamp_to_str function."""
        # Create a timestamp for a known datetime
        test_timestamp = datetime(2023, 12, 25, 15, 30, 45).timestamp()

        result = timestamp_to_str(test_timestamp)

        assert result == "2023-12-25 15:30:45"

    def test_get_cutoff_date(self):
        """Test get_cutoff_date function."""
        # Mock current time to ensure consistent testing
        mock_now = datetime(2023, 12, 25, 15, 30, 45, tzinfo=timezone.utc)

        with patch("jgmd2.util.timeUtil.datetime") as mock_datetime:
            mock_datetime.now.return_value = mock_now
            mock_datetime.combine = datetime.combine
            mock_datetime.min = datetime.min
            mock_datetime.timedelta = timedelta

            result = get_cutoff_date(7)  # 7 days ago

        # Should be 7 days ago at midnight UTC
        expected = datetime(2023, 12, 18, 0, 0, 0, tzinfo=timezone.utc)
        assert result == expected

    def test_get_cutoff_date_zero_days(self):
        """Test get_cutoff_date with zero days."""
        mock_now = datetime(2023, 12, 25, 15, 30, 45, tzinfo=timezone.utc)

        with patch("jgmd2.util.timeUtil.datetime") as mock_datetime:
            mock_datetime.now.return_value = mock_now
            mock_datetime.combine = datetime.combine
            mock_datetime.min = datetime.min
            mock_datetime.timedelta = timedelta

            result = get_cutoff_date(0)

        # Should be today at midnight UTC
        expected = datetime(2023, 12, 25, 0, 0, 0, tzinfo=timezone.utc)
        assert result == expected

    def test_datetimes_are_equal_exact_match(self):
        """Test datetimes_are_equal with exact match."""
        dt1 = datetime(2023, 12, 25, 15, 30, 45)
        dt2 = datetime(2023, 12, 25, 15, 30, 45)

        result = datetimes_are_equal(dt1, dt2)

        assert result is True

    def test_datetimes_are_equal_with_millisecond_allowance(self):
        """Test datetimes_are_equal with millisecond allowance."""
        dt1 = datetime(2023, 12, 25, 15, 30, 45, 100000)  # 100ms
        dt2 = datetime(2023, 12, 25, 15, 30, 45, 200000)  # 200ms

        # Should be equal with 150ms allowance
        result = datetimes_are_equal(dt1, dt2, millisecond_allowance=150)
        assert result is True

        # Should not be equal with 50ms allowance
        result = datetimes_are_equal(dt1, dt2, millisecond_allowance=50)
        assert result is False

    def test_datetimes_are_equal_zero_allowance(self):
        """Test datetimes_are_equal with zero allowance."""
        dt1 = datetime(2023, 12, 25, 15, 30, 45, 100000)
        dt2 = datetime(2023, 12, 25, 15, 30, 45, 200000)

        result = datetimes_are_equal(dt1, dt2, millisecond_allowance=0)
        assert result is False

    def test_datetimes_are_equal_negative_allowance(self):
        """Test datetimes_are_equal with negative allowance."""
        dt1 = datetime(2023, 12, 25, 15, 30, 45)
        dt2 = datetime(2023, 12, 25, 15, 30, 45)

        result = datetimes_are_equal(dt1, dt2, millisecond_allowance=-1)
        assert result is True  # Should still be equal for exact match

    def test_datetimes_are_equal_different_dates(self):
        """Test datetimes_are_equal with different dates."""
        dt1 = datetime(2023, 12, 25, 15, 30, 45)
        dt2 = datetime(2023, 12, 26, 15, 30, 45)

        result = datetimes_are_equal(dt1, dt2, millisecond_allowance=1000)
        assert result is False

    def test_datetimes_are_equal_with_timezone(self):
        """Test datetimes_are_equal with timezone-aware datetimes."""
        dt1 = datetime(2023, 12, 25, 15, 30, 45, tzinfo=timezone.utc)
        dt2 = datetime(2023, 12, 25, 15, 30, 45, tzinfo=timezone.utc)

        result = datetimes_are_equal(dt1, dt2)
        assert result is True

    def test_datetimes_are_equal_mixed_timezone(self):
        """Test datetimes_are_equal with mixed timezone-aware and naive datetimes."""
        dt1 = datetime(2023, 12, 25, 15, 30, 45, tzinfo=timezone.utc)
        dt2 = datetime(2023, 12, 25, 15, 30, 45)  # Naive datetime

        # This should raise TypeError when comparing timezone-aware and naive datetimes
        with pytest.raises(TypeError):
            datetimes_are_equal(dt1, dt2, millisecond_allowance=1000)

    def test_time_it_decorator_preserves_function_metadata(self):
        """Test that time_it decorator preserves function metadata."""

        @time_it
        def test_function():
            """Test function docstring."""
            return "test"

        # Check that function name is preserved
        # Note: The current implementation doesn't preserve metadata
        # This test documents the current behavior
        assert test_function.__name__ == "wrapper"  # Current behavior

        # Check that docstring is not preserved (current behavior)
        assert test_function.__doc__ is None  # Current behavior

    def test_edge_cases_timestamp_conversion(self):
        """Test edge cases for timestamp conversion."""
        # Test with very old timestamp
        old_timestamp = 0  # Unix epoch
        result = seconds_since_timestamp(old_timestamp)
        assert result > 0  # Should be positive (time since epoch)

        # Test with very recent timestamp
        recent_timestamp = time.time() - 0.001  # 1ms ago
        result = seconds_since_timestamp(recent_timestamp)
        assert 0 <= result <= 0.1  # Should be very small positive number
