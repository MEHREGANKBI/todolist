from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import views

app_name = 'accounts'

urlpatterns = [
    path("signin/", TokenObtainPairView.as_view(), name= "sign_in_view"),
    path("tokenRefresh/", TokenRefreshView.as_view(), name= "token_refresh_view"),
    
]