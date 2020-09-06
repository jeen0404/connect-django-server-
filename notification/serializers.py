from rest_framework import serializers

from notification.models import Notification


class FCMTokenSerializer(serializers.Serializer):
    platform = serializers.IntegerField()
    token = serializers.CharField(max_length=1000)
    device = serializers.CharField(max_length=1000)

    class Meta:
        fields = ('platform', 'token')


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'
