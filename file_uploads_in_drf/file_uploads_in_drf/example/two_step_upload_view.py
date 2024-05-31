from drf_spectacular.utils import extend_schema
from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import FileUploadParser, JSONParser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Track


class TrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = ["id", "title", "artist_name", "release_date", "file"]
        read_only_fields = ["id"]


class TrackViewset(ModelViewSet):
    """
    A viewset with a separate action to upload files
    """

    queryset = Track.objects.all()  # pylint: disable=no-member
    serializer_class = TrackSerializer
    parser_classes = [JSONParser]

    @extend_schema(
        operation_id="upload_track",
        request={"application/octet-stream": bytes},
        responses={204: TrackSerializer},
    )
    @action(
        detail=True,
        methods=["POST"],
        parser_classes=[FileUploadParser],
        url_path=r"upload/(?P<filename>[a-zA-Z0-9_]+\.mp3)",
    )
    def upload(self, request, **_kwargs):
        track = self.get_object()

        if "file" not in request.data:
            raise ValidationError("Empty POST data - missing file in the request")

        track_data = TrackSerializer(track).data
        track_data["file"] = request.data["file"]
        serializer = TrackSerializer(instance=track, data=track_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(TrackSerializer(track).data)
