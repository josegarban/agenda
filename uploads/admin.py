# Register your models here.

from django.contrib import admin
from .models import Upload

@admin.register(Upload)
class UploadAdmin(admin.ModelAdmin):
    list_display        = ('username',
                           'uploadtype',
                           'description',
                           'upload',
                           'uploaded_at')
    ordering            = ('uploaded_at',)
