from background_tasks.scheduler import scheduler
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
# Import the VerifyEmailView so we can support legacy /api/verify-email/ endpoints
from users.views import VerifyEmailView

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    
    # Authentication
    path('api/auth/', include('users.urls')),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Chat functionality
    path('api/chat/', include('chat.urls')),
    
    # RAG functionality
    path('api/rag/', include('rag.urls')),

    # Legacy email verification endpoints (some clients may hit /api/verify-email/)
    path('api/verify-email/', VerifyEmailView.as_view(), name='legacy-verify-email'),
    path('api/verify-email/<str:token>/', VerifyEmailView.as_view(), name='legacy-verify-email-with-token'),

]

# Add this to enable background tasks
from background_tasks.scheduler import scheduler