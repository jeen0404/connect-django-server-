from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.generics import CreateAPIView
from accounts.models import UserDetails, User
from accounts.serializers import SearchViewSerializer
from post.serializer import *
import post.models as md


class Post(CreateAPIView):
    """ for handling user_post request """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PostSerializer

    def get(self, request, *args, **kwargs):
        post_id = request.query_params['key']

        # add one more view
        view = md.View()
        view.post_id = post_id
        view.user_id = request.user.user_id
        # view.save()

        post = md.Post.objects.get(post_id=post_id)
        # print(post.user_id)
        # print(post.post_id)
        user = UserDetails.objects.get(user=User.objects.get(user_id='0ac1dc15-c02e-4b35-abe0-8d49898e7be5'))

        likes_count = md.Like.objects.filter(post_id=post_id).count()
        # print(likes_count)
        comments_count = md.Comment.objects.filter(post_id=post_id).count()
        # print(comments_count)
        views_count = md.View.objects.filter(post_id=post_id).count()
        # print(views_count)
        bookmarks_count = md.Bookmark.objects.filter(post_id=post_id).count()
        # print(bookmarks_count)

        likes = LikeSerializer(instance=md.Like.objects.filter(post_id=post_id), many=True).data



        # print('likes',likes)
        comments = CommentSerializer(instance=md.Comment.objects.filter(post_id=post_id), many=True).data
        # print('comments',comments)
        views = ViewSerializer(instance=md.View.objects.filter(post_id=post_id), many=True).data
        # print('views', views)
        tags = TagSerializer(instance=md.Tag.objects.filter(post_id=post_id), many=True).data
        ##print('tags', tags)
        bookmarks = BookmarkSerializer(instance=md.Bookmark.objects.filter(post_id=post_id), many=True).data
        ##print('bookmarks', bookmarks)
        image = ImageSerializer(instance=md.Image.objects.filter(post_id=post_id), many=True).data
        ##print('image', image)

        [x.update(
            {'likes': [],
             'user': SearchViewSerializer(instance=user).data})
            for x in likes]
        [x.update(
            {'comments': None,
             'user': SearchViewSerializer(instance=UserDetails(user=User.objects.get(user_id=x['user_id']))).data})
            for x in comments]
        [x.update(
            {'user': SearchViewSerializer(instance=UserDetails(user=User.objects.get(user_id=x['user_id']))).data})
            for x in views]
        [x.update(
            {'user': SearchViewSerializer(instance=UserDetails(user=User.objects.get(user_id=x['user_id']))).data})
            for x in tags]
        [x.update(
            {'user': SearchViewSerializer(instance=UserDetails(user=User.objects.get(user_id=x['user_id']))).data})
            for x in bookmarks]
        # [x.update(
        #     {'user': SearchViewSerializer(instance=UserDetails(user=User.objects.get(user_id=x['user_id']))).data})
        #     for x in image]
        data = {
            'post_id': post.post_id,
            "user": SearchViewSerializer(instance=user).data,
            "likes_count": str(likes_count),
            "comments_count": str(comments_count),
            "views_count": str(views_count),
            "bookmarks_count": str(bookmarks_count),
            "likes": likes,
            "comments": comments,
            "views": views,
            "tags": tags,
            "bookmarks": bookmarks,
            "images": image,
            'created_at': post.created_at
        }
        return Response(data)


class Like(CreateAPIView):
    """ for handling message request """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LikeSerializer


class Tag(CreateAPIView):
    """ for handling message request """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TagSerializer


class Comment(CreateAPIView):
    """ for handling message request """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CommentSerializer


class View(CreateAPIView):
    """ for handling message request """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ViewSerializer


class Bookmark(CreateAPIView):
    """ for handling message request """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BookmarkSerializer


class Report(CreateAPIView):
    """ for handling message request """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ReportSerializer


class Image(CreateAPIView):
    """ for handling message request """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ImageSerializer
