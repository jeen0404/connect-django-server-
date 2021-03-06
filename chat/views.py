from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.shortcuts import render
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework import permissions
from rest_framework.generics import CreateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from accounts.models import UserDetails, User
from accounts.serializers import SearchViewSerializer
from .models import Conversation, Messages
from .serializers import ConversationSerializer, MessagesSerializer
from rest_framework import permissions, generics, filters

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



class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    max_page_size = 20


class GetUserList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ConversationSerializer
    search_fields = ['user_id', 'post_id']
    # filter_backends = (filters.SearchFilter,)
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return Conversation.objects.filter(sender=self.request.user.user_id, deleted=False).order_by(
            'last_message_time')


# class GetUserList(CreateAPIView):
#     """ for handling follow request """
#     permission_classes = [permissions.IsAuthenticated]
#     serializer_class = ConversationSerializer
#
#     def get(self, request, **kwargs):
#         user = request.user
#         conversation_list = Conversation.objects.filter(sender=user.user_id, deleted=False).order_by(
#             'last_message_time')
#         data = conversation_list.values()
#         for i, j in enumerate(data):
#             j.update({"user": SearchViewSerializer(instance=conversation_list[i].recipient).data,
#                       'last_message_time': str(j['last_message_time']).split('.')[0]})
#         return Response(data)
#
#     def put(self, request, **kwargs):
#         sender = UserDetails(user=User(user_id=request.data['sender_id']))
#         recipient = UserDetails(user=User(user_id=request.data['recipient_id']))
#         print(sender)
#         print(recipient)
#         try:
#             conversion = Conversation.objects.get(sender=sender, recipient=recipient)
#             conversion.unseen_message = 0
#             conversion.save()
#         except Conversation.DoesNotExist as e:
#             print(e)
#         return Response(True)


class GetAllMessages(CreateAPIView):
    """ for handling follow request """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ConversationSerializer

    def post(self, request, **kwargs):
        user = request.user
        conversation_id = request.data['conversation_id']
        conversation_list = Messages.objects.filter(conversation_id=conversation_id, deleted=False)
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
        conversation = Conversation.objects.get(sender=request.user.user_id)
        conversation.unseen_message = 0
        conversation.save()
        return Response(response)


class Message(CreateAPIView):
    """ for handling message request """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MessagesSerializer
    queryset = Messages.objects.all()

    def perform_create(self, serializer):
        serializer.save()
        sender = UserDetails(user=User(user_id=serializer.data['sender_id']))
        recipient = UserDetails(user=User(user_id=serializer.data['recipient_id']))
        print(sender)
        print(recipient)
        try:
            conversion = Conversation.objects.get(sender=sender, recipient=recipient)
            conversion.unseen_message += 1
            conversion.save()
        except Conversation.DoesNotExist as e:
            conversion = Conversation(
                sender=sender,
                recipient=recipient,
                last_message=serializer.data['message'],

            )
            conversion.save()
        try:
            conversion = Conversation.objects.get(sender=recipient, recipient=sender)
            conversion.unseen_message += 1
            conversion.last_message = serializer.data['message']
            conversion.save()
        except Conversation.DoesNotExist as e:
            conversation = Conversation(
                sender=recipient,
                recipient=sender,
                last_message=serializer.data['message'],
                unseen_message=1
            )
            conversation.save()

    def delete(self, request, **kwargs):
        try:
            Messages.objects.get(request.data['message_id'], request.data['sender_id']).delete()
            return Response(True)
        except MultiValueDictKeyError as e:
            return Response(e)
