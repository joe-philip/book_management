from django.contrib.auth.models import User
from rest_framework import serializers


class SignupSerializer(serializers.ModelSerializer):

    def validate_email(self, value: str) -> str:
        value = value.lower()
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                'User with this email already exists'
            )
        return value

    def validate_username(self, value: str) -> str: return value.lower()

    class Meta:
        model = User
        fields = (
            'first_name', 'last_name',
            'username', 'email', 'password'
        )
        extra_kwargs = {
            'password': {'write_only': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
            'email': {'required': True}
        }

    def save(self, **kwargs) -> User:
        password = self.validated_data.pop('password')
        user = User.objects.create_user(**self.validated_data)
        user.set_password(password)
        user.save()
        return user
