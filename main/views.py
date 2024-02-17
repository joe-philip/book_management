from django.contrib.auth.models import User
from django.db.models import QuerySet
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .models import Reviews
from .serializers import (LoginResponseSerializer, LoginSerializer,
                          ReviewSerializer, SignupSerializer)

# Create your views here.


class SignupAPI(CreateAPIView):
    serializer_class = SignupSerializer


class LoginAPI(APIView):
    def post(self, request: Request) -> Response:
        serializer = LoginSerializer(
            data=request.data, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        user: User = serializer.validated_data.get('username')
        if user_token := Token.objects.filter(user=user):
            user_token.delete()
        user_token = Token.objects.create(user=user)
        return Response(
            LoginResponseSerializer(
                user, context={'token': user_token.key}
            ).data
        )


class ReviewsAPI(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = ReviewSerializer

    def get_queryset(self) -> QuerySet[Reviews]:
        Reviews.objects.filter(user=self.request.user)
