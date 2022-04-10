from collections import namedtuple
from dotdict import dotdict

EventEmitter = namedtuple("EventEmitter", ["emit", "on", "off"])


def make_event_emitter():
    callbacks = {}

    def emit(type, payload):
        for func in callbacks.get("*", []):
            func(type, payload)
        for func in callbacks.get(type, []):
            func(payload)

    def on(type, func):
        current_callbacks = callbacks.setdefault(type, [])
        callbacks[type] = [*current_callbacks, func]

    def off(type, func):
        callbacks[type].remove(func)

    return EventEmitter(emit, on, off)


emitter = make_event_emitter()


_event_types = [
    "request_created",
    "request_sent_to_analysis",
    "request_failed_to_be_sent_to_analysis",
]
event_types = dotdict({type: type for type in _event_types})


def log_event(type, payload):
    # https://stackoverflow.com/a/287944
    class bcolors:
        HEADER = "\033[95m"
        OKBLUE = "\033[94m"
        OKCYAN = "\033[96m"
        OKGREEN = "\033[92m"
        WARNING = "\033[93m"
        FAIL = "\033[91m"
        ENDC = "\033[0m"
        BOLD = "\033[1m"
        UNDERLINE = "\033[4m"

    print(
        f"📖 [{bcolors.OKCYAN} {type} {bcolors.ENDC}]: {bcolors.OKBLUE}{str(payload)}{bcolors.ENDC}"
    )


emitter.on("*", log_event)
