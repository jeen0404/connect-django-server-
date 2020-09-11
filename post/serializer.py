from django_cassandra_engine.rest.serializers import DjangoCassandraModelSerializer

from post.models import *


class PostSerializer(DjangoCassandraModelSerializer):
    class Meta:
        model = Post
        exclude = ('created_at', )


class LikeSerializer(DjangoCassandraModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'


class TagSerializer(DjangoCassandraModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class CommentSerializer(DjangoCassandraModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class ViewSerializer(DjangoCassandraModelSerializer):
    class Meta:
        model = View
        fields = '__all__'


class BookmarkSerializer(DjangoCassandraModelSerializer):
    class Meta:
        model = Bookmark
        fields = '__all__'


class ReportSerializer(DjangoCassandraModelSerializer):
    class Meta:
        model = Report
        fields = '__all__'


class ImageSerializer(DjangoCassandraModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'
