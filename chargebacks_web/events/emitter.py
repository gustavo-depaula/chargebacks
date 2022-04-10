from collections import namedtuple

EventEmitter = namedtuple("EventEmitter", ["emit", "on", "off"])


def make_event_emitter():
    callbacks = {}

    def emit(type, payload):
        for func in callbacks.get(type, []):
            func(payload)

    def on(type, func):
        current_callbacks = callbacks.setdefault(type, [])
        callbacks[type] = [*current_callbacks, func]

    def off(type, func):
        callbacks[type].remove(func)

    return EventEmitter(emit, on, off)
