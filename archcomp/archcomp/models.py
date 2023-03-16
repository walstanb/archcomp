from django.db import models

class UploadedFile(models.Model):
    uuid = models.CharField(max_length=255, primary_key=True, editable=False)
    filename = models.CharField(max_length=255)
    folderpath = models.CharField(max_length=255)
    ip_address = models.GenericIPAddressField()
    status = models.CharField(max_length=10, default='pending')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.uuid}"