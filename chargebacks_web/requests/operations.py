#!/usr/bin/env python3

from .models import Request


def list_all_requests():
    return Request.objects.all()


def make_new_request(data):
    Request.objects.create(user_id=data["user_id"], purchase_id=data["purchase_id"])
