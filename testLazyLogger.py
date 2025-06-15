# from jgmd.logging import LazyLogBuffer

from jgmd.logging import FreeTextLogger, LazyLogBuffer


def test_lazy_log_buffer() -> LazyLogBuffer:
    log_buffer = LazyLogBuffer()

    def testFxn():
        print("This test function is called")
        return "Debug message"

    # Add some log entries
    log_buffer.lazyLogDebug(testFxn)
    log_buffer.lazyLogInfo(lambda: "Info message")
    log_buffer.lazyLogWarning(lambda: "Warning message")
    log_buffer.lazyLogError(lambda: "Error message")
    log_buffer.lazyLogSuccessful(lambda: "Success message")

    return log_buffer


if __name__ == "__main__":
    log_buffer = test_lazy_log_buffer()
    print("LazyLogBuffer test passed.")

    logger = FreeTextLogger(
        logDirectory="./logs",
        fileName="test.log",
        logLevel="DEBUG",
    )
    log_buffer.logAll(logger)
