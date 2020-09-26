from django.utils.datetime_safe import datetime
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import permissions, generics, filters
from rest_framework.generics import CreateAPIView
from accounts.models import UserDetails, User
from accounts.serializers import SearchViewSerializer
from post.serializer import *
import post.models as md


class Post(CreateAPIView):
    """ for handling user_post request """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PostSerializer


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 10


class Posts(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer
    search_fields = ['user_id', 'post_id']
    filter_backends = (filters.SearchFilter,)
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return md.Post.objects.filter(user_id=self.request.user.user_id).order_by('-created_at')


class Like(CreateAPIView):
    """ for handling message request """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LikeSerializer


class Tag(CreateAPIView):
    """ for handling message request """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TagSerializer


class Comment(CreateAPIView):
    """ for handling message request """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CommentSerializer


class View(CreateAPIView):
    """ for handling message request """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ViewSerializer


class Bookmark(CreateAPIView):
    """ for handling message request """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BookmarkSerializer


class Report(CreateAPIView):
    """ for handling message request """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ReportSerializer


class Image(CreateAPIView):
    """ for handling message request """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ImageSerializer
