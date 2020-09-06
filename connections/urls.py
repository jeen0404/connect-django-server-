from django.conf.urls import url

from connections.views import FollowView, UnFollowView, GerAllFollowers

app_name = 'connections'
STATIC_ROOT = 'Static'
urlpatterns = [
    url(r'^follow', FollowView.as_view(), name="follow"),
    url(r'^unfollow', UnFollowView.as_view(), name="UnFollow_View"),
    url(r'^GerAllFollowers', GerAllFollowers.as_view(), name="GerAllFollowers"),
]
