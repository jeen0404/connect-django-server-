from rest_framework.serializers import ModelSerializer

from accounts.models import UserDetails
from accounts.serializers import SearchViewSerializer
from .models import Conversation, Messages
from rest_framework import serializers


class ConversationSerializer(ModelSerializer):
    last_message_time = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()
    @classmethod
    def get_last_message_time(self, conversation):
        return str(conversation.last_message_time).split('.')[0]

    @classmethod
    def get_user(self, conversation):
        user_data = UserDetails.objects.get(user=conversation.recipient)
        data = SearchViewSerializer(instance=user_data).data,
        return data[0]

    class Meta:
        model = Conversation
        fields = '__all__'


class MessagesSerializer(ModelSerializer):
    class Meta:
        model = Messages
        fields = '__all__'
