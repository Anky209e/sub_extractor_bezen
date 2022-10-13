
from django.contrib import admin
from django.urls import path,include
from .views import index,video_upload,vid_page
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("",index),
    path("upload/",video_upload,name="upload"),
    path('<str:vid_name>/',vid_page)
]


