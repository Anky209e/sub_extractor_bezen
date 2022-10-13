from .models import ContentVideo
from django.forms import ModelForm

class VideoUploadForm(ModelForm):
    class Meta:
        model  = ContentVideo
        fields = ["name","file"]
