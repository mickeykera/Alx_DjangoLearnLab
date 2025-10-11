from django.contrib import admin
from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipient', 'actor', 'verb', 'unread', 'timestamp')
    list_filter = ('unread',)
    search_fields = ('actor__username', 'recipient__username', 'verb')
