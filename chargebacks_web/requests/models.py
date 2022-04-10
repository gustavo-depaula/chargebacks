from django.db import models
from dotdict import dotdict


class RequestEnum(models.TextChoices):
    received = "rc", "Received"
    in_analysis = "ia", "In Analysis"
    dispatch_failed = "df", "Dispatch Failed"
    accepted = "ac", "Accepted"
    rejected = "rj", "Rejected"


request_transitions = dotdict(
    {
        type: type
        for type in [
            "sent_to_analysis",
            "failed_to_be_sent_to_analysis",
            "approved",
            "rejected",
        ]
    }
)
request_enum_state_machine = {
    RequestEnum.received: {
        "on": {
            request_transitions.sent_to_analysis: RequestEnum.in_analysis,
            request_transitions.failed_to_be_sent_to_analysis: RequestEnum.dispatch_failed,
        }
    },
    RequestEnum.in_analysis: {
        "on": {
            request_transitions.approved: RequestEnum.accepted,
            request_transitions.rejected: RequestEnum.rejected,
        }
    },
    RequestEnum.dispatch_failed: {
        "on": {
            request_transitions.sent_to_analysis: RequestEnum.in_analysis,
        }
    },
    RequestEnum.accepted: {"type": "FINAL"},
    RequestEnum.rejected: {"type": "FINAL"},
}


def request_state_transition(current_state, event):
    is_final_state = (
        request_enum_state_machine[current_state].get("type", "") == "FINAL"
    )
    if is_final_state:
        return current_state

    is_accepted_event = event in request_enum_state_machine[current_state]["on"]
    if not is_accepted_event:
        return current_state

    next_state = request_enum_state_machine[current_state]["on"][event]
    return next_state


class Request(models.Model):
    user_id = models.CharField(max_length=64, db_index=True)
    purchase_id = models.CharField(max_length=64, db_index=True, unique=True)
    state = models.CharField(
        max_length=2, choices=RequestEnum.choices, default=RequestEnum.received
    )
