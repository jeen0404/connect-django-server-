from rest_framework.serializers import ModelSerializer
from .models import Conversation, Messages


class ConversationSerializer(ModelSerializer):
    class Meta:
        model = Conversation
        fields = '__all__'


class MessagesSerializer(ModelSerializer):
    class Meta:
        model = Messages
        fields = '__all__'
