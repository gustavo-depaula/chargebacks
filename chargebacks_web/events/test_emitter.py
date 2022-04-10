from unittest.mock import Mock
from .emitter import make_event_emitter


def test_event_emitter():
    callback = Mock()
    emitter = make_event_emitter()

    emitter.emit("sample_type", {})
    callback.assert_not_called()

    emitter.on("sample_type", callback)
    emitter.emit("sample_type", 2306)
    callback.assert_called_once_with(2306)
    callback.reset_mock()

    emitter.off("sample_type", callback)
    emitter.emit("sample_type", 2306)
    callback.assert_not_called()


def test_event_emitter_wildcard():
    callback = Mock()
    emitter = make_event_emitter()

    emitter.emit("sample_type", {})
    callback.assert_not_called()

    emitter.on("*", callback)
    emitter.emit("sample_type", 2306)
    callback.assert_called_once_with("sample_type", 2306)
    callback.reset_mock()

    emitter.off("*", callback)
    emitter.emit("sample_type", 2306)
    callback.assert_not_called()
