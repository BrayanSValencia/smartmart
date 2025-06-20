# Django imports
from django.contrib.auth import authenticate
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
from django.core.cache import cache
from django.contrib.auth.models import Group

# Third-party imports

from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication


#Simple JWT imports
from rest_framework_simplejwt.tokens import RefreshToken
from jwt import decode as jwt_decode




# Local app imports
from business_logic.serializers.AuthenticationSerializer import RegisterSerializer
from business_logic.serializers.LoginSerializer import LoginSerializer
from business_logic.models.User import AppUser 
from business_logic.models.AccessToken import BlacklistedAccessToken
from business_logic.serializers.UserSerializer import UserSerializer
from business_logic.views.IsSuperUser import IsSuperUser

import uuid
import json
from datetime import datetime



class LoginView(GenericAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(
            request,
            email=serializer.validated_data['email'],
            password=serializer.validated_data['password']
        )

        if (user is None or not user.is_active):
            raise AuthenticationFailed("Invalid credentials or inactive user.")

       # _, token = AuthToken.objects.create(user)
        refresh = RefreshToken.for_user(user)

        return Response({
            'message': 'Successfully logged in',
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        }, status=status.HTTP_200_OK)

class LogoutView(APIView):
    authentication_classes = [JWTAuthentication]

    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Get access token from header
        raw_token = request.headers.get("Authorization", "").split(" ")[1]

        # Decode JWT to get expiration
        payload = jwt_decode(raw_token, settings.SECRET_KEY, algorithms=["HS256"])
        exp_timestamp = payload.get('exp')
        expires_at = datetime.fromtimestamp(exp_timestamp)

        BlacklistedAccessToken.objects.get_or_create(
            token=raw_token,
            defaults={'expires_at': expires_at}
        )
        
        refresh_token_str = request.data.get("refresh")
        if refresh_token_str:
            try:
                refresh_token = RefreshToken(refresh_token_str)
                refresh_token.blacklist()  # This marks it as blacklisted
            except Exception:
                pass  # It's either already blacklisted or invalid
            
        return Response({"message": "Logged out successfully."})


class RegisterView(CreateAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Generate verification token
        verification_token = str(uuid.uuid4())
        
        
        # Store registration data in cache for 5 minutes
        cache.set(
            f"{verification_token}",
            json.dumps(serializer.validated_data),
            timeout=300  # 5 minutes
        )

        # Build verification URL
        verification_url = request.build_absolute_uri(
            reverse('verifyemail', kwargs={'token': verification_token})
        )

        # Send verification email
        send_mail(
            'Complete Your Registration',
            f'Click to complete registration: {verification_url}',
            settings.EMAIL_HOST_USER,
            [serializer.validated_data['email']],
            fail_silently=False,
            html_message=f'<a href="{verification_url}">Complete Registration</a>'
        )

        return Response({
            'message': 'Verification email sent. Please check your inbox.',
        }, status=status.HTTP_202_ACCEPTED)
        
        
class VerifyEmailView(APIView):
    authentication_classes = []
    permission_classes = []


    def get(self, request, token):
        # Retrieve pending registration from cache
        cached_data = cache.get(f"{token}")
        if not cached_data:
            return Response({'error': 'Invalid or expired token'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Parse registration data
        user_data = json.loads(cached_data)
        
        # Create actual user
        user = AppUser.objects.create_user(
           **user_data
        )
        
        # Get or create the "User" group
        user_group, _ = Group.objects.get_or_create(name="User")

        # Assign the user to the group
        user.groups.add(user_group)
        
        # Create auth token
       # _, token = AuthToken.objects.create(user)
        refresh = RefreshToken.for_user(user)
        
        # Clean up cache
        cache.delete(f"{token}")
        
        return Response({
            'message': 'Account created and verified!',
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        }, status=status.HTTP_201_CREATED)
        
        
class CreateStaffUserView(CreateAPIView):
    """
    Only superusers can create staff users.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,IsSuperUser]
    serializer_class = UserSerializer
    queryset = AppUser.objects.all()

    def perform_create(self, serializer):
        user = serializer.save(is_staff=True)
        
        staff_group, _ = Group.objects.get_or_create(name="Staff")
        user.groups.add(staff_group)