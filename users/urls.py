from django.urls import path
from .views import RegisterView, LoginView, VerifyEmailView, UserProfileView, RequestPasswordResetView, ConfirmPasswordResetView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('verify-email/', VerifyEmailView.as_view(), name='verify-email'),
    path('verify-email/<str:token>/', VerifyEmailView.as_view(), name='verify-email-with-token'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('reset-password/request/', RequestPasswordResetView.as_view(), name='request-password-reset'),
    path('reset-password/confirm/<str:token>/', ConfirmPasswordResetView.as_view(), name='confirm-password-reset'),
]