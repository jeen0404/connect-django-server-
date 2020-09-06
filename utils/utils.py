from rest_framework import status
from rest_framework.authtoken.models import Token

from accounts.models import UserDetails, User
from accounts.serializers import ProfileSerializer

STATUS = {
    "status": None,
    "message": None,
}


def too_many_requests():
    STATUS["status"] = status.HTTP_429_TOO_MANY_REQUESTS
    STATUS["message"] = "Reached max limit for the day."
    return (STATUS, STATUS["status"])


def unauthorized():
    STATUS["status"] = status.HTTP_401_UNAUTHORIZED
    STATUS["message"] = "User not logged in."
    return (STATUS, STATUS["status"])


def failure(message="Failed"):
    STATUS["status"] = status.HTTP_400_BAD_REQUEST
    STATUS["message"] = message
    return (STATUS, STATUS["status"])


def success(message=None):
    STATUS["status"] = status.HTTP_200_OK
    STATUS["message"] = message
    return (STATUS, STATUS["status"])


def user_detail(user: User, user_details: UserDetails):
    try:
        token = user.auth_token.key
    except:
        token = Token.objects.create(user=user)
        token = token.key
    user_json = {
        "user_id": user.user_id,
        "token": token,
    }
    if user_details:
        user_json.update({'user_details': ProfileSerializer(instance=user_details).data})
    return user_json


def model_field_attr(model, model_field, attr):
    """
    Returns the specified attribute for the specified field on the model class.
    """
    fields = dict([(field.name, field) for field in model._meta.fields])
    return getattr(fields[model_field], attr)
