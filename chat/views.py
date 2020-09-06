from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.shortcuts import render
from rest_framework import permissions
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from accounts.models import UserDetails, User
from accounts.serializers import SearchViewSerializer
from .models import Conversation, Messages
from .serializers import ConversationSerializer, MessagesSerializer


def index(request):
    return render(request, 'chat/index.html')


def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name': room_name
    })


def send(request, message):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        '{}'.format(request.user.user_id),
        {
            'type': 'channel_message',
            'message': message
        }
    )
    return render(request, "chat/room.html", {
        'room_name': "Done...."
    })


class GetUserList(CreateAPIView):
    """ for handling follow request """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ConversationSerializer

    def get(self, request, **kwargs):
        user = request.user
        conversation_list = Conversation.objects.filter(sender=user.user_id, deleted=False).order_by(
            'last_message_time')
        data = conversation_list.values()
        for i, j in enumerate(data):
            j.update({"user": SearchViewSerializer(instance=conversation_list[i].recipient).data,
                      'last_message_time': str(j['last_message_time']).split('.')[0]})
        return Response(data)

    def put(self, request, **kwargs):
        sender = UserDetails(user=User(user_id=request.data['sender_id']))
        recipient = UserDetails(user=User(user_id=request.data['recipient_id']))
        print(sender)
        print(recipient)
        try:
            conversion = Conversation.objects.get(sender=sender, recipient=recipient)
            conversion.unseen_message = 0
            conversion.save()
        except Conversation.DoesNotExist as e:
            print(e)
        return Response(True)


class GetAllMessages(CreateAPIView):
    """ for handling follow request """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ConversationSerializer

    def post(self, request, **kwargs):
        user = request.user
        conversation_id = request.data['conversation_id']
        conversation_list = Messages.objects.filter(conversation_id=conversation_id, deleted=False).order_by(
            'created_at')
        data = conversation_list.values_list('message_id', 'conversation_id', 'sender_id', 'recipient_id', 'message',
                                             'message_type', 'created_at', 'deleted', 'status')
        response = []
        for i, j in enumerate(data):
            response.append({
                'message_id': str(j[0]),
                'conversation_id': str(j[1]),
                'sender_id': str(j[2]),
                'recipient_id': str(j[3]),
                'message': str(j[4]),
                'message_type': str(j[5]),
                'created_at': str(j[6]).split('.')[0],
                'deleted': str(j[7]),
                'status': str(j[8]),
            })
        return Response(response)


class Message(CreateAPIView):
    """ for handling message request """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MessagesSerializer