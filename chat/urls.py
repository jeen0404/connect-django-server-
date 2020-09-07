from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    path('send/<str:message>/', views.send),
    url('chat_list/', views.GetUserList.as_view(), name='get_user_list'),
    url('messages/', views.GetAllMessages.as_view(), name='get_user_message'),
    url('message/(?P<message_id>[\w\-]+)/$', views.Message.as_view(), name='Message'),
]
