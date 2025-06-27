import time
from datetime import datetime, timezone, timedelta


# create time_it decorator
def time_it(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        time_taken = round(time.time() - start_time, 4)
        print(f"function {func.__name__} took {time_taken} seconds")
        return result

    return wrapper


def seconds_since_timestamp(timestamp: float) -> float:
    current_time = time.time()
    elapsed_time = current_time - timestamp
    return elapsed_time


def seconds_since_datetime(dt: datetime) -> float:
    current_time = datetime.now(timezone.utc) if dt.tzinfo else datetime.now()

    elapsed_time = (current_time - dt).total_seconds()
    return elapsed_time


def subtract_seconds_from_datetime(dt: datetime, seconds: int) -> datetime:
    return dt - timedelta(seconds=seconds)


def datetime_to_str(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def timestamp_to_str(ts: float) -> str:
    return datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")


def get_cutoff_date(days: int) -> datetime:
    cutoff_date = datetime.combine(
        (datetime.now(timezone.utc) - timedelta(days=days)).date(),
        datetime.min.time(),
        tzinfo=timezone.utc,
    )
    return cutoff_date


def datetimes_are_equal(
    dt1: datetime, dt2: datetime, millisecond_allowance: int = 0
) -> bool:
    """
    Compare two datetime objects for equality
    """
    if millisecond_allowance <= 0:
        return dt1 == dt2
    delta_ms = abs((dt1 - dt2).total_seconds() * 1000)
    if delta_ms > millisecond_allowance:
        return False
    return True
