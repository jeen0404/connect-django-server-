import datetime

from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
from fcm_django.models import FCMDevice

USER = get_user_model()


class Notification(models.Model):
    user = models.ForeignKey(USER, on_delete=models.DO_NOTHING)
    icon = models.ImageField(null=True, blank=True, upload_to=f'notification/{str(datetime.datetime.now().date())}')
    title = models.CharField(max_length=100, blank=True)
    sub_title = models.CharField(max_length=250, blank=True)
    type = models.CharField(max_length=20, blank=True)

    def save_and_send_message(self):
        self.save()
        devices = FCMDevice.objects.filter(user=self.user)
        devices.send_message(title=self.title, body=self.sub_title, icon=self.icon.path)
        devices.send_message()
