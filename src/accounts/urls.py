from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import views

app_name = 'accounts'

urlpatterns = [
    path("signin/", TokenObtainPairView.as_view(), name= "sign_in_view"),
    path("tokenRefresh/", views.RefreshTokenWrapper.as_view(), name= "token_refresh_wrapper_view"),
    path("signup/", views.SignupView.as_view(), name= "sign_up_view"),
    path("logout/", views.LogOutView.as_view(), name="log_out_view"),
]