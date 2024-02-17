from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import (CommonPasswordValidator,
                                                     MinimumLengthValidator,
                                                     NumericPasswordValidator)
from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers

from author.models import Authors
from books.models import Books

from .models import Reviews


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


class ReviewSerializer(serializers.ModelSerializer):
    content_type_choices = serializers.ChoiceField(
        choices=Reviews.ContentTypeChoices.choices, write_only=True
    )

    def validate_rating(self, value: int) -> int:
        if value in range(6):
            return value
        raise serializers.ValidationError('Invalid rating')

    def validate(self, attrs):
        if attrs.get('content_type_choices') == 1:
            if not Authors.objects.filter(id=attrs.get('object_id')).exists():
                raise serializers.ValidationError(
                    {'object_id': ['Object not found']}
                )
            previous_review = Reviews.objects.filter(
                content_type__app_label='author',
                content_type__model='authors',
                object_id=attrs.get('object_id'),
                user=self.context.get('request').user
            )
            if self.instance:
                previous_review = previous_review.exclude(id=self.instance.id)
            if previous_review.exists():
                raise serializers.ValidationError('Review already submitted')
        if attrs.get('content_type_choices') == 2:
            if not Books.objects.filter(id=attrs.get('object_id')).exists():
                raise serializers.ValidationError(
                    {'object_id': ['Object not found']}
                )
            previous_review = Reviews.objects.filter(
                content_type__app_label='books',
                content_type__model='books',
                object_id=attrs.get('object_id'),
                user=self.context.get('request').user
            )
            if self.instance:
                previous_review = previous_review.exclude(id=self.instance.id)
            if previous_review.exists():
                raise serializers.ValidationError('Review already submitted')
        return super().validate(attrs)

    class Meta:
        model = Reviews
        fields = '__all__'
        read_only_fields = (
            'slug', 'created_at', 'updated_at', 'object', 'content_type', 'user'
        )

    def save(self, **kwargs):
        content_type_choices = self.validated_data.pop('content_type_choices')
        kwargs['user'] = self.context.get('request').user
        match content_type_choices:
            case 1:
                kwargs['object'] = Authors.objects.get(
                    id=self.validated_data.get('object_id')
                )
                kwargs['content_type'] = ContentType.objects.get(
                    app_label='author', model='authors'
                )
            case 2:
                kwargs['object'] = Books.objects.get(
                    id=self.validated_data.get('object_id')
                )
                kwargs['content_type'] = ContentType.objects.get(
                    app_label='books', model='books'
                )
        return super().save(**kwargs)
