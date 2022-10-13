
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

def home_page(request):
    return redirect('/video')
urlpatterns = [
    path("",home_page),
    path("video/",include("video.urls")),
    path('admin/', admin.site.urls),
]+ static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
