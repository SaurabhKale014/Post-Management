# Custom JWT Auth for manually-managed UserProfile
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import UserProfile

class CustomJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        user_id = validated_token["user_id"]
        try:
            return UserProfile.objects.get(id=user_id)
        except UserProfile.DoesNotExist:
            raise AuthenticationFailed("User not found")