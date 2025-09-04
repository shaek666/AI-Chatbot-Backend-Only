from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model, authenticate
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
import secrets
import string
from .models import EmailVerification
from .serializers import (
    UserRegistrationSerializer, 
    UserLoginSerializer, 
    UserSerializer,
    EmailVerificationSerializer
)

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Explicitly set user as inactive until email verification
        user.is_active = False
        user.is_verified = False
        user.save()
        
        # Create email verification token
        token = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(32))
        expires_at = timezone.now() + timezone.timedelta(hours=24)
        
        EmailVerification.objects.create(
            user=user,
            token=token,
            expires_at=expires_at
        )
        
        # Send verification email (use the correct URL that includes the auth prefix)
        try:
            # build_absolute_uri will respect the current host if available
            verification_url = request.build_absolute_uri(f'/api/auth/verify-email/{token}/')
        except Exception:
            # fallback to localhost if request isn't available for some reason
            verification_url = f"http://localhost:8000/api/auth/verify-email/{token}/"

        send_mail(
            'Verify your email',
            f'Please click the following link to verify your email: {verification_url}',
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False,
        )
        
        return Response({
            'message': 'User registered successfully. Please check your email for verification.',
            'user': UserSerializer(user).data
        }, status=status.HTTP_201_CREATED)

class LoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        
        # Check if user is verified
        if not user.is_verified:
            return Response({
                'non_field_errors': ['Account not verified. Please check your email for verification link.']
            }, status=status.HTTP_400_BAD_REQUEST)
        
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': UserSerializer(user).data
        })

class VerifyEmailView(generics.GenericAPIView):
    serializer_class = EmailVerificationSerializer
    permission_classes = [AllowAny]
    
    def get_token_from_request(self, request):
        """Get token from request data or URL parameter"""
        # Try to get token from request data (POST)
        if request.method == 'POST' and request.data:
            return request.data.get('token')
        
        # Try to get token from URL kwargs
        return self.kwargs.get('token')
    
    def post(self, request, *args, **kwargs):
        """Handle POST requests for API calls"""
        token = self.get_token_from_request(request)
        
        if not token:
            return Response({
                'error': 'Verification token is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        return self._verify_token(token)
    
    def get(self, request, token=None, *args, **kwargs):
        """Handle GET requests for clickable email links"""
        if token is None:
            token = self.kwargs.get('token')
        
        if not token:
            return Response({
                'error': 'Verification token is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        return self._verify_token(token)
    
    def _verify_token(self, token):
        """Common token verification logic"""
        try:
            verification = EmailVerification.objects.get(token=token)
            
            if verification.is_expired():
                return Response({
                    'error': 'Verification token has expired'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            user = verification.user
            user.is_active = True
            user.is_verified = True
            user.save()
            
            verification.delete()
            
            return Response({
                'message': 'Email verified successfully'
            }, status=status.HTTP_200_OK)
            
        except EmailVerification.DoesNotExist:
            return Response({
                'error': 'Invalid verification token'
            }, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user