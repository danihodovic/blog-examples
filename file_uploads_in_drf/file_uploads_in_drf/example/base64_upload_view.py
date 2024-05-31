import mimetypes

import magic
from drf_extra_fields.fields import Base64FileField
from rest_framework import serializers
from rest_framework.parsers import JSONParser
from rest_framework.viewsets import ModelViewSet

from .models import Track


class MP3B64Field(Base64FileField):
    ALLOWED_TYPES = [".mp3"]

    def get_file_extension(self, filename, decoded_file):
        mime = magic.Magic(mime=True)
        mime_type = mime.from_buffer(decoded_file)
        return mimetypes.guess_extension(mime_type)


class TrackBase64Serializer(serializers.ModelSerializer):
    file = MP3B64Field(required=False)

    class Meta:
        model = Track
        fields = ["id", "title", "artist_name", "release_date", "file"]
        read_only_fields = ["id"]


class TrackBase64Viewset(ModelViewSet):
    parser_classes = [JSONParser]
    queryset = Track.objects.all()  # pylint: disable=no-member
    serializer_class = TrackBase64Serializer
