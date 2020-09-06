from django.conf.urls import url
from django.urls import path

from .views import GenerateOTP, ValidateOTP, CheckUsernameAvailability, AddUserDetailsView, SearchUserView, Profile, \
    ViewProfile

app_name = 'accounts'
STATIC_ROOT = 'Static'

urlpatterns = [
    url(r'^generate/$', GenerateOTP.as_view(), name="generate"),
    url(r'^validate/$', ValidateOTP.as_view(), name="validate"),
    url(r'check_username', CheckUsernameAvailability.as_view(), name="check username"),
    url(r'add_profile', AddUserDetailsView.as_view(), name="user_details"),
    url(r'search', SearchUserView.as_view(), name="SearchUserView"),
    path(r'view_profile/<str:username>', ViewProfile.as_view(), name="view profile"),
    url(r'profile', Profile.as_view(), name="Profile"),

]
