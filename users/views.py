from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model, authenticate
from django.utils import timezone
from django.conf import settings
from background_tasks.tasks import send_mail_async
import secrets
import string
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from .models import EmailVerification, PasswordResetToken
from .serializers import (
    UserRegistrationSerializer, 
    UserLoginSerializer, 
    UserSerializer,
    EmailVerificationSerializer,
    PasswordResetRequestSerializer,
    SetNewPasswordSerializer
)

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Set user as active but not verified until email verification
        user.is_active = True
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

        send_mail_async(
            'Verify your email',
            f'Please click the following link to verify your email: {verification_url}',
            settings.EMAIL_HOST_USER,
            [user.email]
        )
        
        return Response({
            'message': 'User registered successfully. Please check your email for verification.',
            'user': UserSerializer(user).data
        }, status=status.HTTP_201_CREATED)

class LoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle]
    
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
    throttle_classes = [AnonRateThrottle]
    
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
    throttle_classes = [UserRateThrottle]
    
    def get_object(self):
        return self.request.user


class RequestPasswordResetView(generics.GenericAPIView):
    serializer_class = PasswordResetRequestSerializer
    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'message': 'If an account with that email exists, a password reset link has been sent.'},
                            status=status.HTTP_200_OK)

        # Delete any existing tokens for this user
        PasswordResetToken.objects.filter(user=user).delete()

        token = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(64))
        expires_at = timezone.now() + timezone.timedelta(hours=1)  # Token valid for 1 hour

        PasswordResetToken.objects.create(
            user=user,
            token=token,
            expires_at=expires_at
        )

        reset_url = request.build_absolute_uri(f'/api/auth/reset-password/confirm/{token}/')

        send_mail_async(
            'Password Reset Request',
            f'Please use the following link to reset your password: {reset_url}',
            settings.EMAIL_HOST_USER,
            [user.email]
        )

        return Response({'message': 'If an account with that email exists, a password reset link has been sent.'},
                        status=status.HTTP_200_OK)


class ConfirmPasswordResetView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer
    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        token = serializer.validated_data['token']
        password = serializer.validated_data['password']

        try:
            reset_token = PasswordResetToken.objects.get(token=token)
        except PasswordResetToken.DoesNotExist:
            return Response({'error': 'Invalid or expired password reset token.'},
                            status=status.HTTP_400_BAD_REQUEST)

        if reset_token.is_expired():
            reset_token.delete()
            return Response({'error': 'Invalid or expired password reset token.'},
                            status=status.HTTP_400_BAD_REQUEST)

        user = reset_token.user
        user.set_password(password)
        user.save()

        reset_token.delete()  # Invalidate the token after use

        return Response({'message': 'Password has been reset successfully.'},
                        status=status.HTTP_200_OK)