import pytest
import asyncio
from jgmd2.events import EventEmitter, EventHandlerError


@pytest.mark.asyncio
async def test_sync_and_async_handlers():
    results = []
    emitter = EventEmitter()

    def sync_handler(event, data):
        results.append(f"sync:{event}:{data}")

    async def async_handler(event, data):
        await asyncio.sleep(0.01)
        results.append(f"async:{event}:{data}")

    emitter.on("test", sync_handler)
    emitter.on("test", async_handler)
    emitter.emit("test", 123)
    await asyncio.sleep(0.05)

    assert "sync:test:123" in results
    assert "async:test:123" in results


def test_listener_management():
    emitter = EventEmitter()
    called = []

    def handler(event, x):
        called.append(x)

    emitter.on("evt", handler)
    assert emitter.has_listeners("evt")
    assert emitter.listener_count("evt") == 1
    emitter.emit("evt", 42)
    assert called == [42]
    assert emitter.off("evt", handler)
    assert not emitter.has_listeners("evt")
    emitter.on("evt", handler)
    emitter.remove_all_listeners("evt")
    assert not emitter.has_listeners("evt")
    emitter.on("evt", handler)
    emitter.remove_all_listeners()
    assert not emitter.has_listeners("evt")


def test_event_validation():
    emitter = EventEmitter(validate_events=True, allowed_events={"foo", "bar"})

    def handler(event, x):
        pass

    emitter.on("foo", handler)
    with pytest.raises(Exception):
        emitter.on("baz", handler)


def test_get_event_names_and_listeners():
    emitter = EventEmitter()

    def h1(event, x):
        pass

    def h2(event, x):
        pass

    emitter.on("a", h1)
    emitter.on("a", h2)
    emitter.on("b", h1)
    names = emitter.get_event_names()
    assert "a" in names and "b" in names
    listeners = emitter.get_listeners("a")
    assert h1 in listeners and h2 in listeners


def test_error_handler_called():
    errors = []

    def error_handler(event, exc):
        errors.append((event, str(exc)))

    emitter = EventEmitter(error_handler=error_handler)

    def bad_handler(event, x):
        raise ValueError("fail")

    emitter.on("err_evt", bad_handler)
    emitter.emit("err_evt", 1)
    assert errors and errors[0][0] == "err_evt"
    assert "fail" in errors[0][1]


def test_error_handler_exception_fallback(capfd):
    def error_handler(event, exc):
        raise RuntimeError("error handler fail")

    emitter = EventEmitter(error_handler=error_handler)

    def bad_handler(event, x):
        raise ValueError("fail")

    emitter.on("evt", bad_handler)
    # Should fallback to stderr print
    emitter.emit("evt", 1)
    out, err = capfd.readouterr()
    assert "error handler fail" in err


def test_event_handler_error_raised():
    emitter = EventEmitter()

    def bad_handler(event, x):
        raise ValueError("fail")

    emitter.on("evt", bad_handler)
    with pytest.raises(EventHandlerError):
        emitter.emit("evt", 1)
