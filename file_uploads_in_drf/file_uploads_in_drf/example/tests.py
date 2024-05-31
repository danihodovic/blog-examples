import base64
import re
from pathlib import Path

import pytest
from django.conf import settings
from django.urls import reverse
from rest_framework.test import APIClient

pytestmark = pytest.mark.django_db


def test_upload_file():
    pass


def test_validates_x():
    pass


def test_b64_file_uploads():
    client = APIClient()
    file_path = settings.BASE_DIR / "file_example_MP3_700KB.mp3"
    file_bytes = base64.b64encode(file_path.read_bytes())
    payload = dict(title="Oko Moje Sanjivo", artist_name="Magazin", file=file_bytes)

    # Create
    list_url = reverse("tracks-b64-list")
    res = client.post(list_url, data=payload, format="json")
    assert res.status_code == 201, res.data

    # Read
    detail_url = reverse("tracks-b64-detail", args=[res.data["id"]])
    res = client.get(detail_url)
    assert res.status_code == 200, res.data
    assert res.data == {
        "id": 1,
        "title": "Oko Moje Sanjivo",
        "artist_name": "Magazin",
        "release_date": None,
        "file": res.data["file"],
    }
    assert re.match(r"http://testserver/media/\w+", res.data["file"])
