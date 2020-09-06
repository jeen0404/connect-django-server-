from django.contrib import admin

from connections.models import Connection, Relation


class ConnectionAdmin(admin.ModelAdmin):
    list_display = ('follower', 'following')
    search_fields = ('follower',)
    list_filter = ('follower',)
    readonly_fields = ('follower', 'following',)


class RelationAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    list_filter = ('name',)
    readonly_fields = ('name',)


admin.site.register(Connection, ConnectionAdmin)
admin.site.register(Relation, RelationAdmin)
