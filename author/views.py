from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet

from .models import Authors
from .serializers import AuthorsSerializer


# Create your views here.
class AuthorsAPI(ModelViewSet):
    queryset = Authors.objects.all()
    serializer_class = AuthorsSerializer
    permission_classes = (IsAdminUser,)
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'
