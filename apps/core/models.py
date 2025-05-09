from django.db import models
from uuid import uuid4

# Create your models here.
class User(models.Model):
    id = models.UUIDField(default=uuid4, editable=False, primary_key=True)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "user"
        verbose_name = "user"
        verbose_name_plural = "users"

    def __str__(self):
        return self.id