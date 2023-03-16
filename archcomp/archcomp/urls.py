"""archcomp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("", views.upload_file, name="upload_file"),
    path("upload", views.upload_file, name="upload_file"),
    path(
        "download/<str:uuid>/<str:filename>", views.download_file, name="download_file"
    ),
    path("api/status/<str:uuid>/", views.get_status, name="get_status"),
    path("admin/", admin.site.urls),
]
