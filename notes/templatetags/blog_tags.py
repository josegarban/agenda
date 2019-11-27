from django import template
from ..models import Post

register = template.Library()

@register.simple_tag
def total_posts():
    return Post.publishedobjects.count()

@register.inclusion_tag('notes/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.publishedobjects.order_by('-published_date')[:count]
    return {'latest_posts': latest_posts}
