from django.urls import path
from . import views

app_name = 'notes'

urlpatterns = [
    path('',
         views.post_list,
         name='post_list'), #root
    path('<int:year>/<int:month>/<int:day>/<slug:post>/',
         views.post_detail,
         name='post_detail'),
    path('post/new/',
         views.post_new,
         name='post_new'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/edit/',
         views.post_edit,
         name='post_edit'),
    path('<int:post_id>/share/',
         views.post_share,
         name='post_share'),
    path('tag/<slug:tag_slug>/',
         views.post_list,
         name='post_list_by_tag'),
    ]
