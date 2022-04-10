from .models import Request, request_state_transition, request_transitions
from events.emitter import emitter, event_types


def list_all_requests():
    return Request.objects.all()


def make_new_request(data):
    request = Request.objects.create(
        user_id=data["user_id"], purchase_id=data["purchase_id"]
    )
    emitter.emit(event_types.request_created, {**data, "request_id": request.id})


def update_request_state(request_id, event):
    request = Request.objects.get(id=request_id)
    next_state = request_state_transition(request.state, event)
    emitter.emit("log", f"Updating request {request_id} to state {next_state}")
    request.state = next_state
    request.save()


def on_request_event(event):
    return lambda payload: update_request_state(payload["request_id"], event)


emitter.on(
    event_types.request_sent_to_analysis,
    on_request_event(request_transitions.sent_to_analysis),
)
emitter.on(
    event_types.request_failed_to_be_sent_to_analysis,
    on_request_event(request_transitions.failed_to_be_sent_to_analysis),
)
