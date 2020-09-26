from django.db import models
from accounts.models import User


class Relation(models.Model):
    relation_id = models.IntegerField(unique=True, auto_created=True, )
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = 'relation'

    def __str__(self):
        return f'{self.name}'


# Create your models here.
class Connection(models.Model):
    follower = models.ForeignKey(User, related_name='follower', on_delete=models.DO_NOTHING)
    following = models.ForeignKey(User, related_name='following', on_delete=models.DO_NOTHING)

    # bloked
    blocked = models.BooleanField(default=False)

    # chat releted setting
    send_message = models.BooleanField(default=True)
    forward_message = models.BooleanField(default=True)
    copy_message = models.BooleanField(default=True)

    # profile releted settings
    view_profile = models.BooleanField(default=True)
    view_followers = models.BooleanField(default=True)
    view_following = models.BooleanField(default=True)
    view_posts = models.BooleanField(default=True)

    # posts releted setting
    commment_on_post = models.BooleanField(default=True)
    like_on_post = models.BooleanField(default=True)
    share_on_post = models.BooleanField(default=True)

    # close friend
    close_friend = models.BooleanField(default=False)

    # secret crush
    secret_crush = models.BooleanField(default=False)

    # secret crush
    # relation = models.ForeignKey(Relation, on_delete=models.DO_NOTHING, default=None, null=True)

    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} : {}".format(
            self.follower.username,
            self.following.username
        )

    class Meta:
        db_table = 'Connections'
