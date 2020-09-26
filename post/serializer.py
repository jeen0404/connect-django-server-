from django.utils.datetime_safe import datetime
from django_cassandra_engine.rest.serializers import DjangoCassandraModelSerializer
from rest_framework import serializers

import post.models  as pm
from accounts.models import UserDetails
from accounts.serializers import SearchViewSerializer


class PostSerializer(DjangoCassandraModelSerializer):
    time_stamp = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    views_count = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()
    @classmethod
    def get_likes(self, post):
        return LikeSerializer(instance=pm.Like.objects.filter(post_id=post.post_id)[0:5], many=True).data

    @classmethod
    def get_tags(self, post):
        return TagSerializer(instance=pm.Tag.objects.filter(post_id=post.post_id)[0:5], many=True).data

    @classmethod
    def get_comments(self, post):
        return CommentSerializer(instance=pm.Comment.objects.filter(post_id=post.post_id)[0:2], many=True).data

    @classmethod
    def get_images(self, post):
        return ImageSerializer(instance=pm.Image.objects.filter(post_id=post.post_id), many=True).data

    @classmethod
    def get_time_stamp(self, post):
        return int(datetime.timestamp(post.created_at))

    @classmethod
    def get_user(self, post):
        print(post.user_id)
        user_data = UserDetails.objects.get(user=post.user_id)
        data = SearchViewSerializer(instance=user_data).data,
        return data[0]

    @classmethod
    def get_likes_count(self, post):
        return str(pm.Like.objects.filter(post_id=post.post_id).count())

    @classmethod
    def get_comments_count(self, post):
        return str(pm.Comment.objects.filter(post_id=post.post_id).count())

    @classmethod
    def get_views_count(self, post):
        return str(pm.View.objects.filter(post_id=post.post_id).count())

    class Meta:
        model = pm.Post
        fields = '__all__'


class LikeSerializer(DjangoCassandraModelSerializer):
    time_stamp = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()

    @classmethod
    def get_likes(self, like):
        return LikeSerializer(instance=pm.Like.objects.filter(post_id=like.like_id)[0:5], many=True).data

    @classmethod
    def get_time_stamp(self, like):
        return int(datetime.timestamp(like.created_at))

    @classmethod
    def get_user(self, like):
        user_data = UserDetails.objects.get(user=like.user_id)
        data = SearchViewSerializer(instance=user_data).data,
        return data[0]

    class Meta:
        model = pm.Like
        fields = '__all__'


class TagSerializer(DjangoCassandraModelSerializer):
    time_stamp = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()

    @classmethod
    def get_time_stamp(self, tag):
        return int(datetime.timestamp(tag.created_at))

    @classmethod
    def get_user(self, tag):
        user_data = UserDetails.objects.get(user=tag.user_id)
        data = SearchViewSerializer(instance=user_data).data,
        return data[0]

    class Meta:
        model = pm.Tag
        fields = '__all__'


class CommentSerializer(DjangoCassandraModelSerializer):
    time_stamp = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()

    @classmethod
    def get_comments(self, like):
        return None

    @classmethod
    def get_time_stamp(self, comment):
        return int(datetime.timestamp(comment.created_at))

    @classmethod
    def get_user(self, comment):
        user_data = UserDetails.objects.get(user=comment.user_id)
        data = SearchViewSerializer(instance=user_data).data,
        return data[0]

    class Meta:
        model = pm.Comment
        fields = '__all__'


class ViewSerializer(DjangoCassandraModelSerializer):
    time_stamp = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()

    @classmethod
    def get_time_stamp(self, comment):
        return int(datetime.timestamp(comment.created_at))

    @classmethod
    def get_user(self, comment):
        user_data = UserDetails.objects.get(user=comment.user_id)
        data = SearchViewSerializer(instance=user_data).data,
        return data[0]

    class Meta:
        model = pm.View
        fields = '__all__'


class BookmarkSerializer(DjangoCassandraModelSerializer):
    time_stamp = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()

    @classmethod
    def get_time_stamp(self, comment):
        return int(datetime.timestamp(comment.created_at))

    @classmethod
    def get_user(self, comment):
        user_data = UserDetails.objects.get(user=comment.user_id)
        data = SearchViewSerializer(instance=user_data).data,
        return data[0]

    class Meta:
        model = pm.Bookmark
        fields = '__all__'


class ReportSerializer(DjangoCassandraModelSerializer):
    class Meta:
        model = pm.Report
        fields = '__all__'


class ImageSerializer(DjangoCassandraModelSerializer):
    time_stamp = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()

    @classmethod
    def get_time_stamp(self, comment):
        return int(datetime.timestamp(comment.created_at))

    @classmethod
    def get_user(self, comment):
        user_data = UserDetails.objects.get(user=comment.user_id)
        data = SearchViewSerializer(instance=user_data).data,
        return data[0]

    class Meta:
        model = pm.Image
        fields = '__all__'
