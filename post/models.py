import uuid
from cassandra.cqlengine import columns
from django.utils import timezone
from django_cassandra_engine.models import DjangoCassandraModel


class Post(DjangoCassandraModel):
    post_id = columns.UUID(primary_key=True, default=uuid.uuid4)
    user_id = columns.UUID(partition_key=True, default=uuid.uuid4)
    can_comment = columns.Boolean(default=True)
    can_share = columns.Boolean(default=True)
    deleted = columns.Boolean(default=False)
    can_bookmark = columns.Boolean(default=True)
    created_at = columns.DateTime(default=timezone.now)

    class Meta:
        get_pk_field = 'post_id'


class Like(DjangoCassandraModel):
    like_id = columns.UUID(primary_key=True, default=uuid.uuid4)
    post_id = columns.UUID(partition_key=True, default=uuid.uuid4)
    user_id = columns.UUID(default=uuid.uuid4)
    deleted = columns.Boolean(default=False)
    created_at = columns.DateTime(default=timezone.now)

    class Meta:
        get_pk_field = 'like_id'


class Tag(DjangoCassandraModel):
    tag_id = columns.UUID(primary_key=True, default=uuid.uuid4)
    post_id = columns.UUID(partition_key=True, default=uuid.uuid4)
    image_id = columns.UUID(default=uuid.uuid4)
    user_id = columns.UUID(default=uuid.uuid4)
    x_axis = columns.Float(default=50)
    y_axis = columns.Float(default=50)
    created_at = columns.DateTime(default=timezone.now)

    class Meta:
        get_pk_field = 'tag_id'


class Comment(DjangoCassandraModel):
    comment_id = columns.UUID(primary_key=True, default=uuid.uuid4)
    post_id = columns.UUID(partition_key=True, default=uuid.uuid4)
    user_id = columns.UUID(default=uuid.uuid4)
    comment = columns.Text(default="")
    deleted = columns.Boolean(default=False)
    created_at = columns.DateTime(default=timezone.now)

    class Meta:
        get_pk_field = 'comment_id'


class View(DjangoCassandraModel):
    view_id = columns.UUID(primary_key=True, default=uuid.uuid4)
    post_id = columns.UUID(partition_key=True, default=uuid.uuid4)
    user_id = columns.UUID(default=uuid.uuid4)
    deleted = columns.Boolean(default=False)
    created_at = columns.DateTime(default=timezone.now)

    class Meta:
        get_pk_field = 'view_id'


class Bookmark(DjangoCassandraModel):
    bookmark_id = columns.UUID(primary_key=True, default=uuid.uuid4)
    post_id = columns.UUID(partition_key=True, default=uuid.uuid4)
    user_id = columns.UUID(default=uuid.uuid4)
    deleted = columns.Boolean(default=False)
    created_at = columns.DateTime(default=timezone.now)

    class Meta:
        get_pk_field = 'bookmark_id'


class Report(DjangoCassandraModel):
    report_id = columns.UUID(primary_key=True, default=uuid.uuid4)
    post_id = columns.UUID(partition_key=True, default=uuid.uuid4)
    user_id = columns.UUID(default=uuid.uuid4)
    deleted = columns.Boolean(default=False)
    report_type = columns.SmallInt()
    note = columns.Text(max_length=500)
    created_at = columns.DateTime(default=timezone.now)

    class Meta:
        get_pk_field = 'report_id'


class Image(DjangoCassandraModel):
    image_id = columns.UUID(primary_key=True, default=uuid.uuid4)
    post_id = columns.UUID(partition_key=True, default=uuid.uuid4)
    user_id = columns.UUID(default=uuid.uuid4)
    deleted = columns.Boolean(default=False)
    height = columns.Integer(default=800)
    width = columns.Integer(default=40)
    ratio = columns.Float(default=0.5)
    url = columns.Text()
    created_at = columns.DateTime(default=timezone.now)

    class Meta:
        get_pk_field = 'image_id'
