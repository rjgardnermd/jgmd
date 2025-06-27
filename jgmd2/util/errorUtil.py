import traceback
from datetime import datetime
from typing import Callable, Tuple


def exception_to_str(e: Exception) -> str:
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    error_message = f"Exception was thrown at {current_time}:\n{''.join(traceback.format_exception(None, e, e.__traceback__))}"
    return error_message


def get_error_handling_decorators(
    on_error: Callable[[str], None],
) -> Tuple[Callable, Callable]:
    def handle_error(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                error_message = exception_to_str(e)
                on_error(error_message)

        return wrapper

    def handle_error_async(func):
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                error_message = exception_to_str(e)
                on_error(error_message)

        return wrapper

    return handle_error, handle_error_async
