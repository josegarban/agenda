from django.urls import path
from . import views

app_name = 'uploads'

urlpatterns = [
                path('delete/<int:id>/',
                     views.user_upload_delete,
                     name='user_upload_delete'),
                path('upload/',
                     views.user_upload_upload,
                     name='user_upload_upload'),
                path('table/',
                     views.user_upload_table,
                     name='user_upload_table'),
                path('',
                     views.user_upload_table,
                     name='user_upload_table'),
              ]
