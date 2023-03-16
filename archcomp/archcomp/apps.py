from django.apps import AppConfig


class ArchcompConfig(AppConfig):
    name = "archcomp"

    def ready(self):
        from .models import UploadedFile
