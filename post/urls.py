from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    url('post/', views.Post.as_view(), name='posts'),
    url('posts/', views.Posts.as_view(), name='posts_list'),
    url('like/', views.Like.as_view(), name='get_user_message'),
    url('tag/', views.Tag.as_view(), name='Message'),
    url('comment/', views.Comment.as_view(), name='Message'),
    url('view/', views.View.as_view(), name='Message'),
    url('bookmark/', views.Bookmark.as_view(), name='Message'),
    url('report/', views.Report.as_view(), name='Message'),
    url('image/', views.Image.as_view(), name='Message'),
]
