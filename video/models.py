from django.db import models
from django.core.validators import FileExtensionValidator

# Create your models here.

class ContentVideo(models.Model):
    name = models.CharField(max_length=30)
    file = models.FileField(upload_to="videos/",validators=[FileExtensionValidator(allowed_extensions=["mp4"])])

    def __str__(self):
        return str(self.name)