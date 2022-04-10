from .models import RequestEnum, request_state_transition, request_transitions


def test_request_state_transition():
    initial_state = RequestEnum.received
    state = request_state_transition(initial_state, "invalid_event")
    assert state == initial_state

    state = request_state_transition(
        state, request_transitions.failed_to_be_sent_to_analysis
    )
    assert state == RequestEnum.dispatch_failed

    state = request_state_transition(state, request_transitions.sent_to_analysis)
    assert state == RequestEnum.in_analysis

    state = request_state_transition(state, request_transitions.approved)
    assert state == RequestEnum.accepted

    state = request_state_transition(state, "any_event")
    state = request_state_transition(state, "any_event")
    assert state == RequestEnum.accepted
