from django.contrib.auth import get_user_model
from rest_flex_fields import FlexFieldsModelSerializer

from .models import Organization

User = get_user_model()


class UserSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "email", "date_joined"]


class OrganizationSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Organization
        fields = ["name", "users"]
        expandable_fields = {"users": (UserSerializer, {"many": True})}
