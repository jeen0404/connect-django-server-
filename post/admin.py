from django.contrib import admin
from .models import *


class PostAdmin(admin.ModelAdmin):
    list_display = ('post_id', 'user_id', 'can_comment', 'can_share', 'deleted', 'can_bookmark')
    search_fields = ('post_id', 'user_id', 'can_comment', 'can_share', 'deleted', 'can_bookmark')
    #list_filter = ('post_id', 'user_id', 'can_comment', 'can_share', 'deleted', 'can_bookmark')


class LikeAdmin(admin.ModelAdmin):
    list_display = ('post_id', 'like_id', 'user_id')
    search_fields = ('post_id', 'like_id', 'user_id')
    #list_filter = ('post_id', 'like_id', 'user_id')


class TagAdmin(admin.ModelAdmin):
    list_display = ('post_id', 'tag_id', 'user_id')
    search_fields = ('post_id', 'tag_id', 'user_id')
    #list_filter = ('post_id', 'tag_id', 'user_id')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('post_id', 'comment_id', 'user_id', )
    search_fields = ('post_id', 'comment_id', 'user_id')
    #list_filter = ('post_id', 'comment_id', 'user_id', 'comment')


class ViewAdmin(admin.ModelAdmin):
    list_display = ('post_id', 'view_id', 'user_id')
    search_fields = ('post_id', 'view_id', 'user_id')
    #list_filter = ('post_id', 'view_id', 'user_id')


class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('post_id', 'bookmark_id', 'user_id')
    search_fields = ('post_id', 'bookmark_id', 'user_id')
    #ist_filter = ('post_id', 'bookmark_id', 'user_id')


class ReportAdmin(admin.ModelAdmin):
    list_display = ('post_id', 'report_id', 'user_id')
    search_fields = ('post_id', 'report_id', 'user_id')
    #list_filter = ('post_id', 'report_id', 'user_id')


class ImageAdmin(admin.ModelAdmin):
    list_display = ('post_id', 'image_id', 'user_id', 'url')
    search_fields = ('post_id', 'image_id', 'user_id', 'url')
    #list_filter = ('post_id', 'image_id', 'user_id', 'url')


admin.site.register(Post, PostAdmin)
admin.site.register(Like, LikeAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Bookmark, BookmarkAdmin)
admin.site.register(View, ViewAdmin)
admin.site.register(Report, ReportAdmin)
admin.site.register(Image, ImageAdmin)
