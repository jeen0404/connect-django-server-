from django.contrib import admin
from .models import Conversation, Messages


class ConversationAdmin(admin.ModelAdmin):
    list_display = ('sender', 'recipient',)
    search_fields = ('sender', 'recipient',)
    list_filter = ('sender', 'recipient',)


class MessagesAdmin(admin.ModelAdmin):
    list_display = ('sender_id', 'recipient_id', 'message',)
    search_fields = ('sender_id', 'recipient_id', 'message',)
    list_filter = ('sender_id', 'recipient_id', 'message',)


admin.site.register(Conversation, ConversationAdmin)
admin.site.register(Messages, MessagesAdmin)
