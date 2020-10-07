from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (RegisterAPIView,
                    PasswordTokenCheckAPIView,
                    RequestPasswordResetEmailAPIView, LoginAPIView, PasswordResetNewPasswordAPIView)

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name="register"),
    path('login/', LoginAPIView.as_view(), name="login"),
    path('token/refresh/', TokenRefreshView.as_view(), name="token-refresh"),
    path('password-reset/<uidb64>/<token>/', PasswordTokenCheckAPIView.as_view(), name="password-reset"),
    path('request-reset-email/', RequestPasswordResetEmailAPIView.as_view(), name="request-reset-email"),
    path('password-reset-setup/', PasswordResetNewPasswordAPIView.as_view(), name="password-reset-setup"),
]
