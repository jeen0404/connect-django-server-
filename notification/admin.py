from django.contrib import admin


# Register your models here.
from notification.models import Notification


class NotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'sub_title', 'type')
    search_fields = ('type',)
    list_filter = ('type',)


admin.site.register(Notification, NotificationAdmin)
