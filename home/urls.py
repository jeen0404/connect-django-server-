from django.conf.urls import url

from home.views import HomeFeed
app_name = 'connections'
STATIC_ROOT = 'Static'
urlpatterns = [
    url(r'^home_feed', HomeFeed.as_view(), name="follow"),
]
