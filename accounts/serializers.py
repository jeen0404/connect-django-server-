from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import PhoneToken, User, UserDetails
from django.core.validators import RegexValidator


class PhoneTokenCreateSerializer(ModelSerializer):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,14}$',
                                 message='Phone no must be in the format of +99999999. 14 digit allowed')
    phone_number = serializers.CharField()

    class Meta:
        model = PhoneToken
        fields = ('pk', 'phone_number')


class PhoneTokenValidateSerializer(ModelSerializer):
    pk = serializers.IntegerField()
    otp = serializers.CharField(max_length=40)

    class Meta:
        model = PhoneToken
        fields = ('pk', 'otp')


class CheckUsernameAvailabilitySerializer(ModelSerializer):
    class Meta:
        model = UserDetails
        fields = ('username',)



class SearchViewSerializer(ModelSerializer):
    class Meta:
        model = UserDetails
        fields = ('user', 'username', 'name', 'profile_image', 'account_verified')


class AddDetailsSerializer(ModelSerializer):
    class Meta:
        model = UserDetails
        fields = ('username', 'name', 'profile_image')


class ProfileSerializer(ModelSerializer):
    class Meta:
        model = UserDetails
        fields = '__all__'
