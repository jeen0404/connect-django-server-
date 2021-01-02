import datetime
import hashlib
import os
import uuid

from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)
from django.utils import timezone
from raindrop import settings


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, phone_number,
                     password, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        if not phone_number:
            raise ValueError('The given username must be set')
        username = self.model.normalize_username(phone_number)
        user = self.model(phone_number=phone_number, user_id=uuid.uuid4(),
                          **extra_fields
                          )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone_number,
                    email=None, password=None, **extra_fields):
        return self._create_user(phone_number, password,
                                 **extra_fields)

    def create_superuser(self, phone_number, password,
                         **extra_fields):
        return self._create_user(phone_number, password,
                                 **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    user_id = models.CharField(max_length=36, unique=True, primary_key=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,14}$',
                                 message='Phone no must be in the format of +99999999. 14 digit allowed', )
    phone_number = models.CharField(validators=[phone_regex], max_length=15, unique=True)
    deleted = models.BooleanField(default=False)
    suspended = models.BooleanField(default=False)
    disabled = models.BooleanField(default=False)
    last_login = None
    username = None
    USERNAME_FIELD = 'phone_number'
    objects = UserManager()

    def __str__(self):  # __unicode__ on Python 2
        return self.phone_number

    def get_username(self):
        return self.phone_number

    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the raindrop `app_label`?"""
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_deleted(self, using=None, keep_parents=False):
        return self.deleted

    @property
    def is_suspended(self):
        return self.suspended

    @property
    def is_disabled(self):
        return self.disabled

    @property
    def is_staff(self):
        return True

    @property
    def is_active(self):
        """Is the user active?"""
        return not any([self.deleted, self.suspended])

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'User'
        db_table = 'users'


# Phone Token authentication
class PhoneToken(models.Model):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,14}$',
                                 message='Phone no must be in the format of +99999999. 14 digit allowed')
    phone_number = models.CharField(validators=[phone_regex], max_length=15)
    otp = models.CharField(max_length=40, editable=False)
    timestamp = models.DateTimeField(auto_now_add=True, editable=False)
    attempts = models.IntegerField(default=0)
    used = models.BooleanField(default=False)

    class Meta:
        verbose_name = "OTP Token"
        verbose_name_plural = "OTP Tokens"
        db_table = 'phone_token'

    def __str__(self):
        return "{} - {}".format(self.phone_number, self.otp)

    @classmethod
    def create_otp_for_number(cls, number):
        # The max otps generated for a number in a day are only 10.
        # Any more than 10 attempts returns False for the day.
        today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
        today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)
        otps = cls.objects.filter(phone_number=number, timestamp__range=(today_min, today_max))
        if otps.count() <= getattr(settings, 'PHONE_LOGIN_ATTEMPTS', 10):
            otp = cls.generate_otp(length=getattr(settings, 'PHONE_LOGIN_OTP_LENGTH', 6))
            phone_token = PhoneToken(phone_number=number, otp=otp)
            phone_token.save()
            # message = send_sms(mobile_no=number, body=SmsTemplates().send_otp(otp))
            return phone_token
        else:
            return False

    @classmethod
    def generate_otp(cls, length=6):
        hash_algorithm = getattr(settings, 'PHONE_LOGIN_OTP_HASH_ALGORITHM', 'sha256')
        m = getattr(hashlib, hash_algorithm)()
        m.update(getattr(settings, 'SECRET_KEY', None).encode('utf-8'))
        m.update(os.urandom(16))
        otp = str(int(m.hexdigest(), 16))[-length:]
        # TODO: change this to actual value later
        return "1234"


class UserDetails(models.Model):
    user = models.OneToOneField(User, unique=True, primary_key=True, on_delete=models.DO_NOTHING)
    username_regex = RegexValidator(regex=r'^[a-zA-Z0-9]+([._]?[a-zA-Z0-9]+)*$',
                                    message='only digits and numbers allowed.', )
    username = models.CharField(unique=True, validators=[username_regex], max_length=50)
    name = models.CharField(max_length=200)
    profession = models.CharField(max_length=200)
    profile_image = models.TextField(default='')

    bio = models.CharField(max_length=250, blank=True, default="")
    birth_date = models.DateField(default=timezone.now)

    # following
    # following = models.ManyToManyField(Connection, related_name='following_id', )
    # follower = models.ManyToManyField(Connection, related_name='follower_id')

    # account verifications
    private = models.BooleanField(default=False)
    account_verified = models.BooleanField(default=False)
    business_profile = models.BooleanField(default=False)

    # settings
    show_followers = models.BooleanField(default=True)
    show_following = models.BooleanField(default=True)
    show_posts = models.BooleanField(default=True)
    show_stores = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'user_details'
        verbose_name_plural = 'user_details'
        db_table = 'user_details'
