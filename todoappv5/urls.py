from django.urls import path

from . import views

app_name="todoappv4"

urlpatterns = [
    path("", views.TaskView.as_view(), name="root"),
    # # The following paths must only be used with their respective functions i.e get and delete, respectively.
    path("get/<str:type_param>/", views.TaskView.as_view(), name = "retrieval_view"),
    path("delete/<int:id_param>/", views.TaskView.as_view(), name = "delete_view"),
    path("signin/", views.CustomAuth.as_view(), name= "sign_in_view"),
    path("signup/", views.CustomAuth.as_view(), name= "sign_up_view")
    ]
