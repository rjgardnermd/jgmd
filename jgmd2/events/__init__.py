"""
Event system for jgmd2.

This module provides a flexible event emitter system that supports both synchronous
and asynchronous event handlers with robust error handling.
"""

from .core.event_emitter import EventEmitter
from .protocols.event_emitter import EventEmitterProtocol
from .exceptions import EventEmitterError, EventHandlerError

__all__ = [
    "EventEmitter",
    "EventEmitterProtocol",
    "EventEmitterError",
    "EventHandlerError",
]
