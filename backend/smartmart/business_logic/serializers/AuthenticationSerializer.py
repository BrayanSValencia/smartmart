from rest_framework import serializers
from business_logic.models import AppUser


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, min_length=8)
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True, max_length=150)
    first_name = serializers.CharField(required=False, max_length=100, allow_blank=True)
    last_name = serializers.CharField(required=False, max_length=100, allow_blank=True)

    class Meta:
        model = AppUser
        fields = ['email', 'username', 'password', 'first_name', 'last_name']

    def validate_email(self, value):
        if AppUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value

    def validate_username(self, value):
        if AppUser.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists")
        return value

    def create(self, validated_data):
        user = AppUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user