# Register your models here.

from django.contrib import admin
from .models import Post
#admin.site.register(Post)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display        = ('title',
                           'slug',
                           'author',
                           'published_date',
                           'status')
    list_filter         = ('status', 'created_date', 'published_date', 'author')
    search_fields       = ('title', 'text')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields       = ('author',)
    date_hierarchy      = 'published_date'
    ordering            = ('status', 'published_date')

# @admin.register(Comment)
# class CommentAdmin(admin.ModelAdmin):
#     list_display  = ('name', 'email', 'post', 'created', 'active')
#     list_filter   = ('active', 'created', 'updated')
#     search_fields = ('name', 'email', 'body')
