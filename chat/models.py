from django.db import models
from accounts.models import UserDetails, User
import uuid
from django.utils import timezone


class Conversation(models.Model):
    sender = models.ForeignKey(UserDetails, related_name="sender", on_delete=models.DO_NOTHING, max_length=36)
    recipient = models.ForeignKey(UserDetails, related_name="recipient", on_delete=models.DO_NOTHING, max_length=36)
    status = models.CharField(default='', max_length=20)
    created_at = models.DateTimeField(auto_now=True, editable=False)
    last_message = models.CharField(max_length=100)
    last_message_time = models.DateTimeField(auto_now=True, editable=True)
    unseen_message = models.IntegerField(default=0)
    deleted = models.BooleanField(default=False)
    froze = models.BooleanField(default=False)


class Messages(models.Model):
    message_id = models.CharField(primary_key=True, default=uuid.uuid4, max_length=36)
    conversation_id = models.ForeignKey(Conversation, on_delete=models.DO_NOTHING, default=None)
    sender_id = models.CharField(max_length=36)
    recipient_id = models.CharField(max_length=36)
    message = models.TextField(max_length=500)
    message_type = models.CharField(max_length=10)
    created_at = models.DateTimeField(default=timezone.now)
    deleted = models.BooleanField(default=False)
    status = models.BooleanField(default=0)
