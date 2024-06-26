# Generated by Django 5.0.6 on 2024-05-29 18:12

from django.db import migrations, models

import file_uploads_in_drf.example.models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Track",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=100)),
                ("artist_name", models.CharField(max_length=100)),
                ("release_date", models.DateField(blank=True, null=True)),
                (
                    "file",
                    models.FileField(
                        blank=True,
                        null=True,
                        upload_to="",
                        validators=[
                            file_uploads_in_drf.example.models.validate_file_size
                        ],
                    ),
                ),
            ],
        ),
    ]
