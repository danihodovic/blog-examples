from rest_framework.routers import DefaultRouter

from .base64_upload_view import TrackBase64Viewset
from .two_step_upload_view import TrackViewset

router = DefaultRouter()


router.register("tracks", TrackViewset, basename="tracks")
router.register("tracks-b64", TrackBase64Viewset, basename="tracks-b64")
