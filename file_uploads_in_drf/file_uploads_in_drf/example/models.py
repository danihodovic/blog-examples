from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models
from sox import file_info
from sox.core import SoxiError


def validate_file_size(file_obj):
    max_size = 1024 * 1024
    if file_obj.size > max_size:
        raise ValidationError(f"File is larger than {max_size=}")


class Track(models.Model):
    title = models.CharField(max_length=100)
    artist_name = models.CharField(max_length=100)
    release_date = models.DateField(blank=True, null=True)
    file = models.FileField(
        null=True,
        blank=True,
        validators=[
            FileExtensionValidator(allowed_extensions=["mp3"]),
            validate_file_size,
        ],
    )

    def __str__(self):
        title = self.title
        id = self.id
        return f"Track {title=} {id=}"
