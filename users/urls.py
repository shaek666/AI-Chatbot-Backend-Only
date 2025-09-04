from django.urls import path
from .views import RegisterView, LoginView, VerifyEmailView, UserProfileView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('verify-email/', VerifyEmailView.as_view(), name='verify-email'),
    path('verify-email/<str:token>/', VerifyEmailView.as_view(), name='verify-email-with-token'),  # ADD THIS LINE
    path('profile/', UserProfileView.as_view(), name='profile'),
]