from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    # single model view
    url('post/', views.Post.as_view(), name='posts'),
    url('like/', views.Like.as_view(), name='get_user_message'),
    url('tag/', views.Tag.as_view(), name='Message'),
    url('comment/', views.Comment.as_view(), name='Message'),
    url('view/', views.View.as_view(), name='Message'),
    url('bookmark/', views.Bookmark.as_view(), name='Message'),
    url('report/', views.Report.as_view(), name='Message'),
    url('image/', views.Image.as_view(), name='Message'),

    # list model view
    url('posts/', views.Posts.as_view(), name='posts_list'),
    url('likes/', views.Likes.as_view(), name='posts_list'),
    url('tags/', views.Tags.as_view(), name='posts_list'),
    url('comments/', views.Comments.as_view(), name='posts_list'),
    url('views/', views.Views.as_view(), name='posts_list'),
    url('bookmarks/', views.Bookmarks.as_view(), name='posts_list'),
    url('reports/', views.Reports.as_view(), name='posts_list'),
    url('images/', views.Images.as_view(), name='posts_list'),
]
