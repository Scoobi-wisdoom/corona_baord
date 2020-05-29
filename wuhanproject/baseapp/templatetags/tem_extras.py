from django import template
from forum.models import *

register = template.Library()

@register.filter
def get_view_count(blogpost_id, blogpost_do):
    blog_post = Post.objects.get(pk=blogpost_id)
    return blog_post.view_count
