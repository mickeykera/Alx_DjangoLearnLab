from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    actor = serializers.StringRelatedField()

    class Meta:
        model = Notification
        fields = ['id', 'actor', 'verb', 'target', 'unread', 'timestamp']
        read_only_fields = ['id', 'actor', 'verb', 'target', 'timestamp']
