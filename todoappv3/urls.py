from django.urls import path

from . import views

app_name="todoappv3"

urlpatterns = [
    path("", views.TodolistCRUDView.as_view(), name="root"),
    # The following paths must only be used with their respective functions i.e get and delete, respectively.
    path("get/<str:type_param>/", views.TodolistCRUDView.as_view(), name = "retrieval_view"),
    path("delete/<int:id_param>/", views.TodolistCRUDView.as_view(), name = "delete_view"),
    ]
