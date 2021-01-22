from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import permissions, generics, filters
from rest_framework.generics import CreateAPIView
from post.serializer import *
import post.models as md


class Post(CreateAPIView):
    """ for handling user_post request """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PostSerializer

    def get(self, request):
        print(self.request.query_params)
        if self.request.query_params.get('post_id'):
            return Response(
                PostSerializer(instance=md.Post.objects.get(post_id=self.request.query_params['post_id'])).data)
        else:
            return Response({'error': "invalid request format"})


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    max_page_size = 20


class Posts(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostListSerializer
    search_fields = ['user_id', 'post_id']
    # filter_backends = (filters.SearchFilter,)
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        user_id = self.request.user.user_id
        if 'user_id' in self.request.query_params and self.request.query_params['user_id'] != self.request.user.user_id:
            user_id = self.request.query_params['user_id']
        data = md.Post.objects.filter(user_id=user_id, deleted=False).order_by('-created_at')
        return data


class Like(CreateAPIView):
    """ for handling message request """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LikeSerializer


class Likes(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LikeSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        if not self.request.query_params.get('post_id'):
            return Response(data={'error': "post id is not in request"})
        post_id = self.request.query_params.get('post_id')
        data = md.Like.objects.filter(post_id=post_id).order_by('-created_at')
        return data


class Tag(CreateAPIView):
    """ for handling message request """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TagSerializer


class Tags(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TagSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        if not self.request.query_params.get('post_id'):
            return Response(data={'error': "post id is not in request"})
        post_id = self.request.query_params.get('post_id')
        data = md.Tag.objects.filter(post_id=post_id).order_by('-created_at')
        return data


class Comment(CreateAPIView):
    """ for handling message request """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CommentSerializer


class Comments(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        if not self.request.query_params.get('post_id'):
            return Response(data={'error': "post id is not in request"})
        post_id = self.request.query_params.get('post_id')
        data = md.Comment.objects.filter(post_id=post_id).order_by('-created_at')
        return data


class View(CreateAPIView):
    """ for handling message request """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ViewSerializer


class Views(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ViewSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        if not self.request.query_params.get('post_id'):
            return Response(data={'error': "post id is not in request"})
        post_id = self.request.query_params.get('post_id')
        data = md.View.objects.filter(post_id=post_id).order_by('-created_at')
        return data


class Bookmark(CreateAPIView):
    """ for handling message request """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BookmarkSerializer


class Bookmarks(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BookmarkSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        if not self.request.query_params.get('post_id'):
            return Response(data={'error': "post id is not in request"})
        post_id = self.request.query_params.get('post_id')
        data = md.Bookmark.objects.filter(post_id=post_id).order_by('-created_at')
        return data


class Report(CreateAPIView):
    """ for handling message request """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ReportSerializer


class Reports(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ReportSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        if not self.request.query_params.get('post_id'):
            return Response(data={'error': "post id is not in request"})
        post_id = self.request.query_params.get('post_id')
        data = md.Report.objects.filter(post_id=post_id).order_by('-created_at')
        return data


class Image(CreateAPIView):
    """ for handling message request """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ImageSerializer


class Images(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ImageSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        if not self.request.query_params.get('post_id'):
            return Response(data={'error': "post id is not in request"})
        post_id = self.request.query_params.get('post_id')
        data = md.Image.objects.filter(post_id=post_id).order_by('-created_at')
        return data
