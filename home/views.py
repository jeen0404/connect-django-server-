from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from post.serializer import PostListSerializer
import post.models as md
from connections import models

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    max_page_size = 20


class HomeFeed(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostListSerializer
    search_fields = ['user_id', 'post_id']
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        following = models.Connection.objects.filter(follower=self.request.user).all().values('following')
        data = md.Post.objects.filter(user_id__in=following, deleted=False).order_by('-created_at')
        return data
