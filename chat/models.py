from django.db import models
from accounts.models import UserDetails, User
import uuid
from cassandra.cqlengine import columns
from django_cassandra_engine.models import DjangoCassandraModel
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


class Messages(DjangoCassandraModel):
    message_id = columns.UUID(primary_key=True, default=uuid.uuid4)
    conversation_id = columns.Text(max_length=72, partition_key=True)
    sender_id = columns.Text(max_length=36)
    recipient_id = columns.Text(max_length=36)
    message = columns.Text(max_length=500)
    message_type = columns.Text(max_length=10)
    created_at = columns.DateTime(default=timezone.now)
    deleted = columns.Boolean(default=False)
    status = columns.SmallInt(default=0)

    class Meta:
        get_pk_field = 'message_id'
