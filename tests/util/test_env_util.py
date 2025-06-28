import os
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock
import pytest
from pydantic import BaseModel
from typing import Optional

from jgmd2.util.envUtil import load_env, load_local_env


class MockEnvConfig(BaseModel):
    """Test Pydantic model for environment variable testing."""

    database_url: str
    api_key: str
    debug_mode: Optional[str] = None
    port: Optional[str] = None


class TestEnvUtil:
    """Test cases for envUtil module."""

    def test_load_env_with_all_required_fields(self):
        """Test loading environment variables with all required fields."""
        with patch.dict(
            os.environ,
            {"database_url": "postgresql://localhost/test", "api_key": "test_key_123"},
        ):
            result = load_env(MockEnvConfig)

            assert isinstance(result, MockEnvConfig)
            assert result.database_url == "postgresql://localhost/test"
            assert result.api_key == "test_key_123"
            assert result.debug_mode is None
            assert result.port is None

    def test_load_env_with_optional_fields(self):
        """Test loading environment variables with optional fields."""
        with patch.dict(
            os.environ,
            {
                "database_url": "postgresql://localhost/test",
                "api_key": "test_key_123",
                "debug_mode": "true",
                "port": "8080",
            },
        ):
            result = load_env(MockEnvConfig)

            assert isinstance(result, MockEnvConfig)
            assert result.database_url == "postgresql://localhost/test"
            assert result.api_key == "test_key_123"
            assert result.debug_mode == "true"
            assert result.port == "8080"

    def test_load_env_with_missing_required_fields(self):
        """Test loading environment variables with missing required fields."""
        with patch.dict(
            os.environ,
            {
                "database_url": "postgresql://localhost/test"
                # Missing api_key
            },
        ):
            with pytest.raises(Exception):  # Pydantic validation error
                load_env(MockEnvConfig)

    def test_load_env_with_dotenv_path(self):
        """Test loading environment variables from a specific .env file."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".env", delete=False) as f:
            f.write("database_url=postgresql://localhost/test\n")
            f.write("api_key=test_key_123\n")
            f.write("debug_mode=true\n")
            dotenv_path = f.name

        try:
            result = load_env(MockEnvConfig, dotenv_path=dotenv_path)

            assert isinstance(result, MockEnvConfig)
            assert result.database_url == "postgresql://localhost/test"
            assert result.api_key == "test_key_123"
            assert result.debug_mode == "true"
        finally:
            os.unlink(dotenv_path)

    def test_load_env_override_existing_env_vars(self):
        """Test that dotenv file overrides existing environment variables."""
        with patch.dict(
            os.environ, {"database_url": "original_url", "api_key": "original_key"}
        ):
            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".env", delete=False
            ) as f:
                f.write("database_url=overridden_url\n")
                f.write("api_key=overridden_key\n")
                dotenv_path = f.name

            try:
                result = load_env(MockEnvConfig, dotenv_path=dotenv_path)

                assert result.database_url == "overridden_url"
                assert result.api_key == "overridden_key"
            finally:
                os.unlink(dotenv_path)

    def test_load_local_env(self):
        """Test loading environment variables from a .env file co-located with a file."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create a test file
            test_file = Path(temp_dir) / "test_script.py"
            test_file.write_text("# test script")

            # Create a .env file in the same directory
            env_file = Path(temp_dir) / ".env"
            env_file.write_text(
                "database_url=postgresql://localhost/test\napi_key=test_key_123\n"
            )

            result = load_local_env(MockEnvConfig, str(test_file))

            assert isinstance(result, MockEnvConfig)
            assert result.database_url == "postgresql://localhost/test"
            assert result.api_key == "test_key_123"

    def test_load_local_env_with_file_path(self):
        """Test load_local_env with a specific file path."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create a test file
            test_file = Path(temp_dir) / "subdir" / "test_script.py"
            test_file.parent.mkdir()
            test_file.write_text("# test script")

            # Create a .env file in the parent directory
            env_file = Path(temp_dir) / ".env"
            env_file.write_text(
                "database_url=postgresql://localhost/test\napi_key=test_key_123\n"
            )

            result = load_local_env(MockEnvConfig, str(test_file))

            assert isinstance(result, MockEnvConfig)
            assert result.database_url == "postgresql://localhost/test"
            assert result.api_key == "test_key_123"

    def test_load_env_with_complex_pydantic_model(self):
        """Test loading environment variables with a more complex Pydantic model."""

        class ComplexConfig(BaseModel):
            app_name: str
            version: str
            database: str
            redis_url: Optional[str] = None
            max_connections: Optional[str] = None

        with patch.dict(
            os.environ,
            {
                "app_name": "test_app",
                "version": "1.0.0",
                "database": "postgresql://localhost/test",
                "redis_url": "redis://localhost:6379",
                "max_connections": "100",
            },
        ):
            result = load_env(ComplexConfig)

            assert isinstance(result, ComplexConfig)
            assert result.app_name == "test_app"
            assert result.version == "1.0.0"
            assert result.database == "postgresql://localhost/test"
            assert result.redis_url == "redis://localhost:6379"
            assert result.max_connections == "100"

    def test_load_env_with_empty_optional_fields(self):
        """Test loading environment variables with empty optional fields."""
        with patch.dict(
            os.environ,
            {
                "database_url": "postgresql://localhost/test",
                "api_key": "test_key_123",
                "debug_mode": "",
                "port": "",
            },
        ):
            result = load_env(MockEnvConfig)

            assert isinstance(result, MockEnvConfig)
            assert result.database_url == "postgresql://localhost/test"
            assert result.api_key == "test_key_123"
            assert result.debug_mode == ""
            assert result.port == ""
