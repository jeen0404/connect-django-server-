from rest_framework.serializers import ModelSerializer

from accounts.models import UserDetails
from accounts.serializers import SearchViewSerializer
from post.models import *
from rest_framework import serializers
from datetime import datetime


class PostSerializer(ModelSerializer):
    user = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    views_count = serializers.SerializerMethodField()

    @classmethod
    def get_user(self, post):
        user_data = UserDetails.objects.get(user=post.user_id)
        data = SearchViewSerializer(instance=user_data).data,
        return data[0]

    @classmethod
    def get_likes_count(self, post):
        return str(Like.objects.filter(post_id=post.post_id).count())

    @classmethod
    def get_comments_count(self, post):
        return str(Comment.objects.filter(post_id=post.post_id).count())

    @classmethod
    def get_views_count(self, post):
        return str(View.objects.filter(post_id=post.post_id).count())

    class Meta:
        model = Post
        fields = '__all__'


class PostListSerializer(ModelSerializer):
    user = serializers.SerializerMethodField()

    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    views_count = serializers.SerializerMethodField()

    @classmethod
    def get_likes_count(self, post):
        return str(Like.objects.filter(post_id=post.post_id).count())

    @classmethod
    def get_comments_count(self, post):
        return str(Comment.objects.filter(post_id=post.post_id).count())

    @classmethod
    def get_views_count(self, post):
        return str(View.objects.filter(post_id=post.post_id).count())
    @classmethod
    def get_user(self, tag):
        user_data = UserDetails.objects.get(user=tag.user_id)
        data = SearchViewSerializer(instance=user_data).data,
        return data[0]

    class Meta:
        model = Post
        fields = '__all__'


class LikeSerializer(ModelSerializer):
    user = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()

    @classmethod
    def get_likes(self, like):
        return LikeSerializer(instance=Like.objects.filter(post_id=like.like_id)[0:5], many=True).data

    @classmethod
    def get_user(self, like):
        user_data = UserDetails.objects.get(user=like.user_id)
        data = SearchViewSerializer(instance=user_data).data,
        return data[0]

    class Meta:
        model = Like
        fields = '__all__'


class TagSerializer(ModelSerializer):
    user = serializers.SerializerMethodField()

    @classmethod
    def get_user(self, tag):
        user_data = UserDetails.objects.get(user=tag.user_id)
        data = SearchViewSerializer(instance=user_data).data,
        return data[0]

    class Meta:
        model = Tag
        fields = '__all__'


class CommentSerializer(ModelSerializer):
    user = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()

    @classmethod
    def get_comments(self, like):
        return None

    @classmethod
    def get_user(self, comment):
        user_data = UserDetails.objects.get(user=comment.user_id)
        data = SearchViewSerializer(instance=user_data).data,
        return data[0]

    class Meta:
        model = Comment
        fields = '__all__'


class ViewSerializer(ModelSerializer):
    user = serializers.SerializerMethodField()

    @classmethod
    def get_user(self, comment):
        user_data = UserDetails.objects.get(user=comment.user_id)
        data = SearchViewSerializer(instance=user_data).data,
        return data[0]

    class Meta:
        model = View
        fields = '__all__'


class BookmarkSerializer(ModelSerializer):
    user = serializers.SerializerMethodField()

    @classmethod
    def get_user(self, comment):
        user_data = UserDetails.objects.get(user=comment.user_id)
        data = SearchViewSerializer(instance=user_data).data,
        return data[0]

    class Meta:
        model = Bookmark
        fields = '__all__'


class ReportSerializer(ModelSerializer):
    class Meta:
        model = Report
        fields = '__all__'


class ImageSerializer(ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'
