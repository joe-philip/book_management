from rest_framework.generics import CreateAPIView

from .serializers import SignupSerializer

# Create your views here.


class SignupAPI(CreateAPIView):
    serializer_class = SignupSerializer
