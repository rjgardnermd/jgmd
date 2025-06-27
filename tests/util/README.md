# jgmd2.util Unit Tests

This directory contains comprehensive unit tests for all functions in the `jgmd2.util` module.

## Test Files

- `test_env_util.py` - Tests for environment variable loading functions
- `test_error_util.py` - Tests for error handling and exception utilities  
- `test_file_util.py` - Tests for file and directory utilities
- `test_time_util.py` - Tests for time and datetime utilities

## Running Tests

Just run pytest from the project root:

```bash
pytest tests/util/
```

Or run specific test files:

```bash
pytest tests/util/test_env_util.py
pytest tests/util/test_error_util.py
pytest tests/util/test_file_util.py
pytest tests/util/test_time_util.py
```

## Test Coverage

The tests cover all functions in the util modules:

### envUtil
- `load_env()` - Loading environment variables into Pydantic models
- `load_local_env()` - Loading from co-located .env files

### errorUtil
- `exception_to_str()` - Converting exceptions to formatted strings
- `get_error_handling_decorators()` - Creating error handling decorators

### fileUtil
- `ensure_dir_exists()` - Creating directories and nested directory structures

### timeUtil
- `time_it()` - Function timing decorator
- `seconds_since_timestamp()` - Time calculations from timestamps
- `seconds_since_datetime()` - Time calculations from datetime objects
- `subtract_seconds_from_datetime()` - DateTime arithmetic
- `datetime_to_str()` - DateTime formatting
- `timestamp_to_str()` - Timestamp formatting
- `get_cutoff_date()` - Date cutoff calculations
- `datetimes_are_equal()` - DateTime comparison with tolerance

## Test Features

- **Comprehensive Coverage**: All functions and edge cases are tested
- **Async Support**: Tests for both sync and async error handling
- **Integration Tests**: Tests showing how utilities work together
- **Mocking**: Uses unittest.mock for isolated testing
- **Temporary Files**: Uses tempfile for safe file operations
- **Error Conditions**: Tests various error scenarios and edge cases

## Requirements

- pytest
- pytest-asyncio (for async tests)
- pytest-cov (for coverage reports)

## Adding New Tests

When adding new functions to the util modules:

1. Add unit tests to the appropriate test file
2. Add integration tests to `test_all_util.py` if the function interacts with other utilities
3. Update this README if needed
4. Ensure all tests pass before committing

## Test Markers

Tests are marked with:
- `@pytest.mark.unit` - Unit tests
- `@pytest.mark.integration` - Integration tests
- `@pytest.mark.asyncio` - Async tests
- `@pytest.mark.slow` - Tests that take longer to run 