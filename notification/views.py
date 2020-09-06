from django.core.exceptions import ObjectDoesNotExist
from fcm_django.models import FCMDevice
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from accounts.models import UserDetails
from notification.models import Notification
from notification.serializers import FCMTokenSerializer, NotificationSerializer


class AddFcmToken(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FCMTokenSerializer

    def post(self, request, **kwargs):
        ser = self.serializer_class(
            data=request.data,
            context={'request': request}
        )
        if ser.is_valid():
            try:
                device = FCMDevice.objects.get(device_id=request.data['device'])
                device.registration_id = request.data['token']
                device.save()
                return Response(True, status=status.HTTP_200_OK)
            except ObjectDoesNotExist as e:
                fcm_device = FCMDevice()
                user_details: UserDetails = UserDetails.objects.get(user=request.user)
                fcm_device.name = user_details.username
                fcm_device.user = request.user
                fcm_device.device_id = request.data['device']
                fcm_device.registration_id = request.data['token']
                fcm_device.type = 'ios' if request.data['platform'] == 2 else 'android' if request.data[
                                                                                               'platform'] == 1 else 'web'
                fcm_device.save()
            return Response(True, status=status.HTTP_200_OK)
        return Response(False, status=status.HTTP_200_OK)


class NotificationView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationSerializer

    def get(self, request, **kwargs):
        id = request.GET.get('id', 1)
        data = Notification.objects.filter(user=request.user, **{'id__gte': id})
        data = data.values()
        [d.update({'index': d['id']}) for d in data]
        return Response(data)
