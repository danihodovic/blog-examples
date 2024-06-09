from uuid import uuid4

from drf_spectacular.utils import (
    OpenApiRequest,
    OpenApiResponse,
    extend_schema,
    inline_serializer,
)
from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import FileUploadParser, JSONParser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import TrackS3


class TrackS3Serializer(serializers.ModelSerializer):
    class Meta:
        model = TrackS3
        fields = ["id", "title", "artist_name", "file"]
        read_only_fields = ["id"]


class TrackS3Viewset(ModelViewSet):
    """
    A viewset backend with an S3 store
    """

    queryset = TrackS3.objects.all()  # pylint: disable=no-member
    serializer_class = TrackS3Serializer
    parser_classes = [JSONParser]

    @extend_schema(
        operation_id="upload_track",
        request={"application/octet-stream": bytes},
        responses={204: TrackS3Serializer},
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

        track_data = TrackS3Serializer(track).data
        track_data["file"] = request.data["file"]
        serializer = TrackS3Serializer(instance=track, data=track_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(TrackS3Serializer(track).data)

    @extend_schema(
        operation_id="generate_presigned_url",
        request=OpenApiRequest(),
        responses={
            200: OpenApiResponse(
                inline_serializer(
                    "generate_presigned_url_response",
                    fields=dict(url=serializers.URLField()),
                )
            )
        },
    )
    @action(
        detail=True,
        methods=["POST"],
        url_path="presigned-url",
    )
    def presigned_url(self, _request, **_kwargs):
        track = self.get_object()
        bucket = track.file.storage.bucket_name
        key = str(uuid4())
        upload_url = track.file.storage.connection.meta.client.generate_presigned_url(
            "put_object", Params={"Bucket": bucket, "Key": key}
        )

        track.file.name = key
        track.save()
        return Response({"url": upload_url})
