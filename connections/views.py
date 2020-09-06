from rest_framework import status
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework import permissions
# Create your views here.
from accounts.models import UserDetails
from notification.models import Notification
from .serializers import (
    FollowSerializer, GetAllFollowerSerializer, ConnectionSerializer,
)
from django.contrib.auth import get_user_model

User = get_user_model()

from .models import Connection


class FollowView(CreateAPIView):
    """ for handling follow request """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FollowSerializer

    def get(self, request, **kwargs):
        print('kwargs', kwargs)
        print(request.GET)
        try:
            follower = request.user
            following = UserDetails.objects.get(username=request.GET['username'])
            try:
                connection = Connection.objects.get(follower=follower, following=following.user)
                data = ConnectionSerializer(instance=connection).data
                data.update({'username': request.GET['username']})
                return Response(data, status=status.HTTP_200_OK)
            except Connection.DoesNotExist as e:
                return Response(None, status=status.HTTP_200_OK)
        except UserDetails.DoesNotExist as e:
            return Response(None, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, format=False, **kwargs):
        return Response({'reason': 'delete request is not supported yet', }, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, **kwargs):
        try:
            follower = request.user
            following = UserDetails.objects.get(username=request.data['username'])
            try:
                connection = Connection.objects.get(follower=follower, following=following.user)
                if connection.blocked:
                    # user is blocked id follower
                    return Response({'reason': "user is blocked"}, status=status.HTTP_406_NOT_ACCEPTABLE)
                else:
                    return Response({'reason': "already following"}, status=status.HTTP_226_IM_USED)
            except Connection.DoesNotExist as e:
                connection = Connection(follower=follower, following=following.user)
                connection.save()
                data = ConnectionSerializer(instance=connection).data
                data = data.update({'username': request.data['username']})
                # send notification
                try:
                    notification = Notification()
                    user_details = UserDetails.objects.get(user=request.user)
                    notification.title = user_details.username
                    notification.user = following.user
                    notification.sub_title = user_details.name + " started following you"
                    notification.type = 'follow'
                    notification.icon = following.profile_image
                    Notification.objects.filter(user=following.user, type='follow', title=user_details.username).delete()
                    notification.save_and_send_message()
                except:
                    print("Error in notification send")
                return Response(data, status=status.HTTP_200_OK)
        except User.DoesNotExist as e:
            return Response({'reason': "User name is not exist", 'error': str(e)}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, **kwargs):
        try:
            follower = request.user
            following = UserDetails.objects.get(username=request.data['username'])
            try:
                connection = Connection.objects.get(follower=follower, following=following.user)
                if connection.blocked:
                    # user is blocked id follower
                    return Response({'reason': "user is blocked"}, status=status.HTTP_406_NOT_ACCEPTABLE)
                else:
                    connection.delete()
                    return Response(True, status=status.HTTP_226_IM_USED)
            except Connection.DoesNotExist as e:
                return Response({'reason': "not connection exist"}, status=status.HTTP_200_OK)
        except User.DoesNotExist as e:
            return Response({'reason': "User name is not exist", 'error': str(e)}, status=status.HTTP_404_NOT_FOUND)


class UnFollowView(CreateAPIView):
    """ for handling unfollow request """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FollowSerializer

    def post(self, request, format=False, **kwargs):
        print('request', request.data)
        try:
            follower = request.user
            following = User.objects.get(username=request.data['username'])
            # check if user alrady exsit or blocked
            try:
                connection = Connection.objects.get(follower=follower, following=following)
                if connection.blocked == True:
                    return Response({'reason': f"you'r not following {following}"}, status=status.HTTP_200_OK)
                else:
                    connection.delete()
                   # delete old notification wich is send fro follow
                   # user_details = UserDetails.objects.get(user=request.user)
                   # Notification.objects.filter(user=following, type='follow', title=user_details.username).delete()
                return Response({'sucess': f"{following} is unfollowed succesfully"}, status=status.HTTP_200_OK)
            except Connection.DoesNotExist as e:
                return Response({'reason': f"you'r not following  {following}"}, status=status.HTTP_200_OK)

        except User.DoesNotExist as e:
            return Response({'reason': "User name is not exist", 'error': str(e)}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, format=False):
        return Response({'reason': 'delete request is not supported yet', }, status=status.HTTP_400_BAD_REQUEST)


from django.forms.models import model_to_dict


class GerAllFollowers(GenericAPIView):
    """ for handling un_follow request """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GetAllFollowerSerializer

    def get(self, request):
        return Response(Connection.objects.row("SELECT "))
