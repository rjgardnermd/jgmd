import time
from datetime import datetime, timezone, timedelta, time


# create timeIt decorator
def timeIt(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        timeTaken = round(time.time() - start_time, 4)
        print(f"function {func.__name__} took {timeTaken} seconds")
        return result

    return wrapper


def secondsSinceTimestamp(timestamp: float) -> float:
    current_time = time.time()
    elapsed_time = current_time - timestamp
    return elapsed_time


def secondsSinceDatetime(dt: datetime) -> float:
    current_time = datetime.now(timezone.utc) if dt.tzinfo else datetime.now()

    elapsed_time = (current_time - dt).total_seconds()
    return elapsed_time


def subtractSecondsFromDatetime(dt: datetime, seconds: int) -> datetime:
    return dt - timedelta(seconds=seconds)


def datetimeToStr(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def timestampToStr(ts: float) -> str:
    return datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")


def getCutoffDate(days: int) -> datetime:
    cutoffDate = datetime.combine(
        (datetime.now(timezone.utc) - timedelta(days=days)).date(),
        datetime.min.time(),
        tzinfo=timezone.utc,
    )
    return cutoffDate


def datetimesAreEqual(
    dt1: datetime, dt2: datetime, millisecondAllowance: int = 0
) -> bool:
    """
    Compare two datetime objects for equality
    """
    if millisecondAllowance <= 0:
        return dt1 == dt2
    deltaMs = abs((dt1 - dt2).total_seconds() * 1000)
    if deltaMs > millisecondAllowance:
        return False
    return True
