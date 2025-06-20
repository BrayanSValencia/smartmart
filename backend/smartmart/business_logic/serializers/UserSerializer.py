from business_logic.models.User import AppUser
from rest_framework import serializers
from django.contrib.auth.hashers import make_password


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = AppUser
        fields = ['email', 'username', 'password', 'first_name', 'last_name', 'phone', 'date_of_birth', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

    def create(self, validated_data):
        # Hash the password manually
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)