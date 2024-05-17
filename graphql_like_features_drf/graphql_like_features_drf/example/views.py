from django.contrib.auth import get_user_model
from rest_framework.routers import DefaultRouter
from rest_framework.viewsets import ModelViewSet

from .models import Organization
from .serializers import OrganizationSerializer, UserSerializer

User = get_user_model()


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class OrganizationViewset(ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer


router = DefaultRouter()


router.register("users", UserViewSet)
router.register("organizations", OrganizationViewset)
