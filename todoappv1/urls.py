from django.urls import path

from . import views

app_name = "todoappv1"

urlpatterns = [
    path("", views.index, name="index"),
    path("retrieve_all/", views.retrieve_all, name="retrieve_all_todolist"),
    path("retrieve_undone/", views.retrieve_undone, name = "retrieve_undone_todolist"),
    path("done/<int:id_param>/", views.done, name="status_done"),
    path("add_activity/<str:activity_param>/", views.add_activity, name = "add_activity"),
    path("remove_activity/<int:id_param>/", views.remove_activity, name = "remove_activity")
]
