from django.db import models


class RequestEnum(models.TextChoices):
    received = "rc", "Received"
    in_analysis = "ia", "In Analysis"
    accepted = "ac", "Accepted"
    rejected = "rj", "Rejected"


class Request(models.Model):
    user_id = models.CharField(max_length=64, db_index=True)
    purchase_id = models.CharField(max_length=64, db_index=True, unique=True)
    state = models.CharField(
        max_length=2, choices=RequestEnum.choices, default=RequestEnum.received
    )
