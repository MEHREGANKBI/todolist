from django.urls import path

from . import views

app_name="todoappv2"

urlpatterns = [
    path("", views.TodolistCRUDView.as_view(), name="todoappv2_root"),
    ]
