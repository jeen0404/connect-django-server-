from django.conf import settings
from django.contrib.auth import authenticate, login
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status, generics
from rest_framework.generics import CreateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from twilio.base.exceptions import TwilioRestException
from rest_framework import filters
from utils.utils import user_detail
from .models import PhoneToken, UserDetails, User
from connections.models import Connection
from .serializers import (
    PhoneTokenCreateSerializer, PhoneTokenValidateSerializer, CheckUsernameAvailabilitySerializer, AddDetailsSerializer,
    SearchViewSerializer, ProfileSerializer
)

from fcm_django.models import FCMDevice


class GenerateOTP(CreateAPIView):
    """ generate otp or send otp for login """
    # queryset = PhoneToken.objects.all()
    serializer_class = PhoneTokenCreateSerializer

    def post(self, request, format=None, **kwargs):
        # Get the patient if present or result None.
        #print('request', request.data)
        ser = self.serializer_class(
            data=request.data,
            context={'request': request}
        )
        if ser.is_valid():
            try:
                token = PhoneToken.create_otp_for_number(
                    request.data.get('phone_number')
                )
                if token:
                    phone_token = self.serializer_class(
                        token, context={'request': request}
                    )
                    data = phone_token.data
                    if getattr(settings, 'PHONE_LOGIN_DEBUG', False):
                        data['debug'] = token.otp
                    return Response(data)
                return Response({
                    'reason': "you can not have more than {n} attempts per day, please try again tomorrow".format(
                        n=getattr(settings, 'PHONE_LOGIN_ATTEMPTS', 10))}, status=status.HTTP_403_FORBIDDEN)
            except TwilioRestException as e:
                return Response({'reason': "Please enter a valid mobile no.", 'error': str(e)},
                                status=status.HTTP_200_OK, )
        return Response(
            {'reason': ser.errors}, status=status.HTTP_406_NOT_ACCEPTABLE)


class ValidateOTP(CreateAPIView):
    """ validate otp """
    queryset = PhoneToken.objects.all()
    serializer_class = PhoneTokenValidateSerializer

    def post(self, request, format=None, **kwargs):
        # Get the patient if present or result None.
        ser = self.serializer_class(
            data=request.data, context={'request': request}
        )
        if ser.is_valid():
            pk = request.data.get("pk")
            otp = request.data.get("otp")
            try:
                user = authenticate(request, pk=pk, otp=otp)
                login(request, user)
                try:
                    user_details = UserDetails.objects.get(user=user)
                    #print('user_details', user_details.user)
                except Exception as e:
                    #print(e)
                    user_details = None
                response = user_detail(user, user_details)

                if user_details:
                    follower = Connection.objects.filter(follower=user).count()
                    following = Connection.objects.filter(following=user).count()
                    response['user_details'].update(
                        {'follower': str(follower), 'following': str(following), 'post': '0'})

                return Response(response, status=status.HTTP_200_OK)
            except ObjectDoesNotExist as e:
                return Response(
                    {'reason': "OTP doesn't exist. Please enter valid OTP"},
                    status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION
                )
        return Response(
            {'reason': ser.errors}, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)


class CheckUsernameAvailability(CreateAPIView):
    """ check user name is available or not """
    serializer_class = CheckUsernameAvailabilitySerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, **kwargs):
        #print('data', request.data)
        ser = self.serializer_class(
            data=request.data, context={'request': request}
        )
        if ser.is_valid():
            return Response(True, status=status.HTTP_200_OK)
        return Response(False, status=status.HTTP_226_IM_USED)


class AddUserDetailsView(CreateAPIView):
    """  only for first time login """
    """ it will add new user in user details table """
    permission_classes = [IsAuthenticated]
    serializer_class = AddDetailsSerializer
    queryset = UserDetails.objects.all()

    def post(self, request, **kwargs):
        #print('data', request.data)
        ser = self.serializer_class(
            data=request.data, context={'request': request}
        )
        if ser.is_valid() or True:
            user = UserDetails()
            user.user = request.user
            user.username = request.data.get('username')
            user.name = request.data.get('name')
            profile_image = request.data.get('profile_image')
            profile_image.name = request.user.user_id + '.' + profile_image.name.split('.')[-1]
            user.profile_image = profile_image
            user.save()
            return Response(True, status=status.HTTP_200_OK)
        else:
            return Response(False, status=status.HTTP_226_IM_USED)


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 10


class SearchUserView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = UserDetails.objects.all()
    search_fields = ['username', 'name']
    filter_backends = (filters.SearchFilter,)
    serializer_class = SearchViewSerializer
    pagination_class = StandardResultsSetPagination


class Profile(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer

    def get(self, request):
        data = UserDetails.objects.get(user=request.user)
        data = self.serializer_class(instance=data).data
        follower = Connection.objects.filter(following=request.user, ).count()
        following = Connection.objects.filter(follower=request.user).count()
        data.update({'follower': str(follower), 'following': str(following), 'post': '20'})

        return Response(data)


class ViewProfile(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer

    def get(self, request, **kwargs):
        print('username----------------------------------------------------', )
        try:
            data = UserDetails.objects.get(username=kwargs['username'])
            follower = Connection.objects.filter(following=data.user).count()
            following = Connection.objects.filter(follower=data.user).count()
            data = self.serializer_class(instance=data).data
            data.update({'follower': str(follower), 'following': str(following), 'post': '0'})
        except ObjectDoesNotExist as e:
            data = {'reason': "user not exist", 'error': str(e)}

        return Response(data)



