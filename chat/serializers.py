from django_cassandra_engine.rest.serializers import DjangoCassandraModelSerializer
from rest_framework.fields import CharField
from rest_framework.serializers import ModelSerializer
from .models import Conversation, Messages
from rest_framework import serializers


class ConversationSerializer(ModelSerializer):
    class Meta:
        model = Conversation
        fields = '__all__'


class MessagesSerializer(DjangoCassandraModelSerializer):
    class Meta:
        model = Messages
        fields = '__all__'
