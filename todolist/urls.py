"""
URL configuration for todolist project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("todoappv4/", include("todoappv4.urls"), name = "todoappv4urls"),
    path("todoappv3/", include("todoappv3.urls"), name = "todoappv3urls"),
    path("todoappv2/", include("todoappv2.urls"), name = "todoappv2urls"),
    path("todoappv1/", include("todoappv1.urls"), name = "todoappv1urls"),
    path("admin/", admin.site.urls),
]
