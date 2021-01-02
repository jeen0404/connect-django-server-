import uuid
from django.utils import timezone
from django.db import models
from accounts.models import User


class Post(models.Model):
    post_id = models.CharField(primary_key=True, default=uuid.uuid4, max_length=36)
    user_id = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    can_comment = models.BooleanField(default=True)
    can_share = models.BooleanField(default=True)
    deleted = models.BooleanField(default=False)
    can_bookmark = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)


class Like(models.Model):
    like_id = models.CharField(primary_key=True, default=uuid.uuid4, max_length=36)
    post_id = models.ForeignKey(Post, on_delete=models.DO_NOTHING)
    user_id = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)


class Comment(models.Model):
    comment_id = models.CharField(primary_key=True, default=uuid.uuid4, max_length=36)
    post_id = models.ForeignKey(Post, on_delete=models.DO_NOTHING)
    user_id = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    comment = models.TextField(default="")
    deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)


class View(models.Model):
    view_id = models.CharField(primary_key=True, default=uuid.uuid4, max_length=36)
    post_id = models.ForeignKey(Post, on_delete=models.DO_NOTHING)
    user_id = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)


class Bookmark(models.Model):
    bookmark_id = models.CharField(primary_key=True, default=uuid.uuid4, max_length=36)
    post_id = models.ForeignKey(Post, on_delete=models.DO_NOTHING)
    user_id = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)


class Report(models.Model):
    report_id = models.CharField(primary_key=True, default=uuid.uuid4, max_length=36)
    post_id = models.ForeignKey(Post, on_delete=models.DO_NOTHING)
    user_id = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    deleted = models.BooleanField(default=False)
    report_type = models.IntegerField()
    note = models.TextField(max_length=500)
    created_at = models.DateTimeField(default=timezone.now)


class Image(models.Model):
    image_id = models.CharField(primary_key=True, default=uuid.uuid4,max_length=36)
    post_id = models.ForeignKey(Post, on_delete=models.DO_NOTHING)
    user_id = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    deleted = models.BooleanField(default=False)
    height = models.IntegerField(default=800)
    width = models.IntegerField(default=40)
    ratio = models.FloatField(default=0.5)
    url = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)


class Tag(models.Model):
    tag_id = models.CharField(primary_key=True, default=uuid.uuid4,max_length=36)
    post_id = models.ForeignKey(Post, models.DO_NOTHING)
    image_id = models.ForeignKey(Image, models.DO_NOTHING)
    user_id = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    x_axis = models.FloatField(default=50)
    y_axis = models.FloatField(default=50)
    created_at = models.DateTimeField(default=timezone.now)
