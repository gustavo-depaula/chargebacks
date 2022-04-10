from django.urls import path

from . import views

app_name = "requests"
urlpatterns = [path("", views.index, name="index"), path("new", views.new, name="new")]
