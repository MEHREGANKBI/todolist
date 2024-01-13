from django.urls import path

from . import views

app_name="todoappv5"

urlpatterns = [
    path("", views.TaskView.as_view(), name="root"),
    # # The following paths must only be used with their respective functions i.e get and delete, respectively.
    path("get/", views.TaskView.as_view(), name = "retrieval_view"),
    path("delete/<int:id_param>/", views.TaskView.as_view(), name = "delete_view"),
    ]
