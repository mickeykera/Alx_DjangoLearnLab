from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import Post, Comment

User = get_user_model()


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "post", "author", "content", "created_at", "updated_at"]
        read_only_fields = ["id", "author", "created_at", "updated_at"]


class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ["id", "author", "title", "content", "created_at", "updated_at", "comments"]
        read_only_fields = ["id", "author", "created_at", "updated_at", "comments"]

    def create(self, validated_data):
        request = self.context.get("request")
        user = None
        if request and hasattr(request, "user"):
            user = request.user
        return Post.objects.create(author=user, **validated_data)
        # Removed stray end patch comment