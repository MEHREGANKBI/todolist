from django.urls import path

from . import views

app_name="todoappv3"

urlpatterns = [
    path("", views.TodolistCRUDView.as_view(), name="root"),
    path("<int:id_param>/", views.TodolistCRUDView.as_view(), name = "delete_view"),
    path("<str:type_param>/", views.TodolistCRUDView.as_view(), name = "retrieval_view"),
    
    ]
