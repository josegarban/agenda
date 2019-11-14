from django.db import models

from django.db import models
from django.contrib.auth.models import User

from django.db.models.signals import pre_save

from datetime import datetime
#########

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<username>/<filename>
    _datetime = datetime.now()
    timestamp = _datetime.strftime("%Y%m%d%H%M%S")
    return '{0}/{1}_{2}_{3}'.format(instance.username, instance.uploadtype, timestamp, filename)


class Upload(models.Model):
    UPLOADTYPES_CHOICES = (
        ('99', 'Not classified'),
        ('11', 'Document'),
        ('21', 'Editable document'),
        ('31', 'Picture'),
        ('41', 'Video'),
        )

    username    = models.CharField(max_length=10, blank=True, verbose_name="User name")
    uploadtype  = models.CharField(max_length=120, default='99', choices= UPLOADTYPES_CHOICES, verbose_name="Upload type")
    description = models.CharField(max_length=255, blank=True, verbose_name="Description")
    upload      = models.FileField(upload_to=user_directory_path, verbose_name="Path")
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="Loaded on")

    def __str__(self):
        return str(self.upload)

    def delete(self, *args, **kwargs):
        self.Upload.delete()
        super(Upload, self).delete()
