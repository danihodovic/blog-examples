from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Organization(models.Model):
    name = models.CharField(max_length=50)
    users = models.ManyToManyField(to=User)

    def __str__(self):
        return f"Organization {self.name} ({self.id})"
