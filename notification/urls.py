from django.conf.urls import url
from django.urls import path

from .views import AddFcmToken, NotificationView

app_name = 'notification'
STATIC_ROOT = 'Static'

urlpatterns = [
    url(r'add_fcm_token', AddFcmToken.as_view(), name="fcm"),
    url(r'', NotificationView.as_view(), name="notification"),

]
