from django.urls import path
from .views import (
    create_blog_view,
    detail_blog_view,
    edit_blog_view,
    delete_blog_view,
    delete_comment_view,
    post_list_view,
    up_vote_view,
)

app_name = 'forum'

urlpatterns = [
    path('', post_list_view, name="post_list"),
    path('create/', create_blog_view, name="create"),
    path('<id>/<title>/', detail_blog_view, name="detail"),
    path('<id>/<title>/edit/', edit_blog_view, name="edit"),
    path('<id>/<title>/delete/', delete_blog_view, name='delete'),

    # comments
    path('<id>/<title>/comment/<cid>/delete', delete_comment_view, name='comment_delete'),

    # vote
    path('up/<id>/<title>', up_vote_view, name='up_vote'),

]
