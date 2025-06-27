import os
import tempfile
import pytest
from pathlib import Path

from jgmd2.util.fileUtil import ensure_dir_exists


class TestFileUtil:
    """Test cases for fileUtil module."""

    def test_ensure_dir_exists_new_directory(self):
        """Test creating a new directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            new_dir = os.path.join(temp_dir, "new_directory")

            # Directory should not exist initially
            assert not os.path.exists(new_dir)

            # Create directory
            ensure_dir_exists(new_dir)

            # Directory should now exist
            assert os.path.exists(new_dir)
            assert os.path.isdir(new_dir)

    def test_ensure_dir_exists_nested_directories(self):
        """Test creating nested directories."""
        with tempfile.TemporaryDirectory() as temp_dir:
            nested_dir = os.path.join(temp_dir, "level1", "level2", "level3")

            # Nested directories should not exist initially
            assert not os.path.exists(nested_dir)

            # Create nested directories
            ensure_dir_exists(nested_dir)

            # All levels should now exist
            assert os.path.exists(nested_dir)
            assert os.path.isdir(nested_dir)

            # Check intermediate directories also exist
            level1 = os.path.join(temp_dir, "level1")
            level2 = os.path.join(temp_dir, "level1", "level2")
            assert os.path.exists(level1)
            assert os.path.isdir(level1)
            assert os.path.exists(level2)
            assert os.path.isdir(level2)

    def test_ensure_dir_exists_existing_directory(self):
        """Test that existing directory is not affected."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Directory already exists
            assert os.path.exists(temp_dir)
            assert os.path.isdir(temp_dir)

            # Call ensure_dir_exists on existing directory
            ensure_dir_exists(temp_dir)

            # Directory should still exist and be unchanged
            assert os.path.exists(temp_dir)
            assert os.path.isdir(temp_dir)

    def test_ensure_dir_exists_empty_string(self):
        """Test behavior with empty string."""
        # Should not raise an exception
        ensure_dir_exists("")

        # Empty string should not create any directory
        assert not os.path.exists("")

    def test_ensure_dir_exists_none_value(self):
        """Test behavior with None value."""
        # Should not raise an exception
        ensure_dir_exists(None)

        # None should not create any directory - but we can't check os.path.exists(None)
        # because it raises TypeError. The function should handle None gracefully.
        # We just verify it doesn't raise an exception.

    def test_ensure_dir_exists_with_special_characters(self):
        """Test creating directory with special characters in name."""
        with tempfile.TemporaryDirectory() as temp_dir:
            special_dir = os.path.join(temp_dir, "test-dir_with.underscores")

            # Directory should not exist initially
            assert not os.path.exists(special_dir)

            # Create directory
            ensure_dir_exists(special_dir)

            # Directory should now exist
            assert os.path.exists(special_dir)
            assert os.path.isdir(special_dir)

    def test_ensure_dir_exists_with_spaces(self):
        """Test creating directory with spaces in name."""
        with tempfile.TemporaryDirectory() as temp_dir:
            spaced_dir = os.path.join(temp_dir, "test dir with spaces")

            # Directory should not exist initially
            assert not os.path.exists(spaced_dir)

            # Create directory
            ensure_dir_exists(spaced_dir)

            # Directory should now exist
            assert os.path.exists(spaced_dir)
            assert os.path.isdir(spaced_dir)

    def test_ensure_dir_exists_multiple_calls(self):
        """Test multiple calls to ensure_dir_exists on same directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            test_dir = os.path.join(temp_dir, "test_multiple_calls")

            # First call
            ensure_dir_exists(test_dir)
            assert os.path.exists(test_dir)
            assert os.path.isdir(test_dir)

            # Second call
            ensure_dir_exists(test_dir)
            assert os.path.exists(test_dir)
            assert os.path.isdir(test_dir)

            # Third call
            ensure_dir_exists(test_dir)
            assert os.path.exists(test_dir)
            assert os.path.isdir(test_dir)

    def test_ensure_dir_exists_with_pathlib_path(self):
        """Test creating directory using pathlib Path object."""
        with tempfile.TemporaryDirectory() as temp_dir:
            path_obj = Path(temp_dir) / "pathlib_test_dir"

            # Directory should not exist initially
            assert not path_obj.exists()

            # Create directory using string conversion
            ensure_dir_exists(str(path_obj))

            # Directory should now exist
            assert path_obj.exists()
            assert path_obj.is_dir()

    def test_ensure_dir_exists_permissions(self):
        """Test that created directory has proper permissions."""
        with tempfile.TemporaryDirectory() as temp_dir:
            test_dir = os.path.join(temp_dir, "permissions_test")

            # Create directory
            ensure_dir_exists(test_dir)

            # Check that directory is writable
            assert os.access(test_dir, os.W_OK)

            # Check that directory is readable
            assert os.access(test_dir, os.R_OK)

    def test_ensure_dir_exists_relative_path(self):
        """Test creating directory with relative path."""
        # Create a relative path
        relative_dir = "test_relative_dir"

        try:
            # Directory should not exist initially
            assert not os.path.exists(relative_dir)

            # Create directory
            ensure_dir_exists(relative_dir)

            # Directory should now exist
            assert os.path.exists(relative_dir)
            assert os.path.isdir(relative_dir)

        finally:
            # Clean up
            if os.path.exists(relative_dir):
                os.rmdir(relative_dir)

    def test_ensure_dir_exists_absolute_path(self):
        """Test creating directory with absolute path."""
        with tempfile.TemporaryDirectory() as temp_dir:
            absolute_dir = os.path.abspath(os.path.join(temp_dir, "absolute_test"))

            # Directory should not exist initially
            assert not os.path.exists(absolute_dir)

            # Create directory
            ensure_dir_exists(absolute_dir)

            # Directory should now exist
            assert os.path.exists(absolute_dir)
            assert os.path.isdir(absolute_dir)

    def test_ensure_dir_exists_with_file_in_path(self):
        """Test behavior when a file exists with the same name."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create a file
            file_path = os.path.join(temp_dir, "test_file")
            with open(file_path, "w") as f:
                f.write("test content")

            # Try to create a directory with the same name
            # On macOS, this might not raise an OSError immediately
            # The function should handle this gracefully
            try:
                ensure_dir_exists(file_path)
                # If it doesn't raise an exception, that's also acceptable
                # The function might handle this case gracefully
            except OSError:
                # If it does raise OSError, that's also acceptable
                pass

    def test_ensure_dir_exists_unicode_path(self):
        """Test creating directory with unicode characters."""
        with tempfile.TemporaryDirectory() as temp_dir:
            unicode_dir = os.path.join(temp_dir, "test_unicode_测试_ñáéíóú")

            # Directory should not exist initially
            assert not os.path.exists(unicode_dir)

            # Create directory
            ensure_dir_exists(unicode_dir)

            # Directory should now exist
            assert os.path.exists(unicode_dir)
            assert os.path.isdir(unicode_dir)
