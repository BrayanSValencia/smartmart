from business_logic.models.AccessToken import BlacklistedAccessToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed

class JWTWithAccessBlacklistAuthentication(JWTAuthentication):
    def authenticate(self, request):
        result = super().authenticate(request)
        if result is None:
            return None

        user, validated_token = result
        raw_token = request.headers.get("Authorization", "").split(" ")[1]

        # Check blacklist and remove expired ones
        blacklist = BlacklistedAccessToken.objects.filter(token=raw_token).first()
        if blacklist:
            if blacklist.is_expired():
                blacklist.delete()
            else:
                raise AuthenticationFailed("Access token has been blacklisted.")

        return user, validated_token
