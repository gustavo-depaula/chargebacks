from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
import os, binascii
from .operations import make_new_request, list_all_requests

# Create your views here.
def index(request):
    return render(request, "requests/index.html", {"requests": list_all_requests()})


def new(request):
    make_random_string = lambda: str(binascii.b2a_hex(os.urandom(15)))
    make_new_request(
        {"user_id": make_random_string(), "purchase_id": make_random_string()}
    )
    return HttpResponseRedirect(reverse("requests:index"))
