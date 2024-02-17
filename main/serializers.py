from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import (CommonPasswordValidator,
                                                     MinimumLengthValidator,
                                                     NumericPasswordValidator)
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

    def validate_password(self, value: str) -> str:
        validators = (
            CommonPasswordValidator(), MinimumLengthValidator(), NumericPasswordValidator()
        )
        tuple(map(lambda x: x.validate(value), validators))
        return value

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


class LoginSerializer(serializers.Serializer):
    username = serializers.SlugRelatedField(
        queryset=User.objects.all(), slug_field='username',
        error_messages={'does_not_exist': 'User not found'}
    )
    password = serializers.CharField()

    def validate(self, attrs):
        if authenticate(self.context.get('request'), username=attrs.get('username').username, password=attrs.get('password')):
            return super().validate(attrs)
        raise serializers.ValidationError('Invalid credentials')


class LoginResponseSerializer(serializers.ModelSerializer):
    auth_token = serializers.SerializerMethodField()

    def get_auth_token(self, instance: User) -> dict | None:
        return self.context.get('token')

    class Meta:
        model = User
        exclude = ('password',)
