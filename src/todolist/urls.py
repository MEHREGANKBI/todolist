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
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

urlpatterns = [
    path("account/", include("accounts.urls"), name= "account_urls"),
    path("todoappv5/", include("todoappv5.urls"), name = "todoappv5urls"),
    path("todoappv4/", include("todoappv4.urls"), name = "todoappv4urls"),
    path("admin/", admin.site.urls),
]


handler500 = "exception_handler.custom_exception_handlers.django_custom_handler_500"

handler400 = "exception_handler.custom_exception_handlers.django_custom_handler_400"

handler404 = "exception_handler.custom_exception_handlers.django_custom_handler_404"

handler403 = "exception_handler.custom_exception_handlers.django_custom_handler_403"