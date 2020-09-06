from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from connections.models import Connection


class FollowSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)


class GetAllFollowerSerializer(ModelSerializer):
    class Meta:
        model = Connection
        fields = ('following',)


class ConnectionSerializer(ModelSerializer):
    class Meta:
        model = Connection
        exclude = ('follower', 'following')
