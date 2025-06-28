#!/usr/bin/env python3

import sys
from jgmd2.events import EventEmitter


def test_error_handler_fallback():
    print("Testing error handler fallback...")

    def error_handler(event, exc):
        print(f"Error handler called with: event='{event}', exc={exc}")
        print(f"Exception type: {type(exc)}")
        print(f"Exception args: {exc.args}")
        print(f"Exception repr: {repr(exc)}")
        raise RuntimeError("error handler fail")

    emitter = EventEmitter(error_handler=error_handler)

    def bad_handler(event, x):
        print(f"Bad handler called with: {event}, {x}")
        raise ValueError("fail")

    emitter.on("evt", bad_handler)
    print("About to emit event...")
    emitter.emit("evt", 1)
    print("Event emitted.")


if __name__ == "__main__":
    test_error_handler_fallback()
