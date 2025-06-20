# Third-party imports
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView, 
    UpdateAPIView, 
    DestroyAPIView
)

#Django
from django.conf import settings


#SimpleJWT authentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from jwt import decode as jwt_decode
from rest_framework_simplejwt.tokens import RefreshToken

#local imports
from business_logic.models import AppUser
from business_logic.serializers.UserSerializer import UserSerializer
from business_logic.views.IsOwner import IsOwner
from business_logic.views.IsSuperUser import IsSuperUser
from business_logic.models.AccessToken import BlacklistedAccessToken

from datetime import datetime


class RetrieveUserView(RetrieveAPIView):
    """
    Retrieve the current authenticated user
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,IsOwner]
    serializer_class = UserSerializer

    def get_object(self):
        return AppUser.objects.get(pk=self.request.user.pk)  #Fetch a fresh copy from DB using the pk 
        

class UpdateUserView(UpdateAPIView):
    """
    Partially update the current authenticated user
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,IsOwner]
    serializer_class = UserSerializer

    def get_object(self):
        return AppUser.objects.get(pk=self.request.user.pk)

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True  # allow partial update
        return super().update(request, *args, **kwargs)


class DeactivateUserAccount(UpdateAPIView):
    """
    Deactivate the logged account
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,IsOwner]

    def get_object(self):
        return AppUser.objects.get(pk=self.request.user.pk)

    def update(self, request):
        user = self.get_object()
        user.is_active = False  #Deactivate account
        user.save()
        
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
            
        return Response({"detail": "Account deactivated successfully."})
    


class ListUserView(ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,IsSuperUser]
    query_set=AppUser.objects.all
    serializer_class = AppUser



class DeleteUserView(DestroyAPIView):
    """
     Delete an user with the pk (Only superuser)
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,IsSuperUser]
    serializer_class = UserSerializer  

    def get_object(self):
        pk=self.kwargs.get("pk")
        return AppUser.objects.get(pk=pk)

    def destroy(self):
        user = self.get_object()
        user.delete()
        return Response({"message": "User deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    
    
