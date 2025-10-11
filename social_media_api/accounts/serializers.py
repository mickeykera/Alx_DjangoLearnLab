from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers
from rest_framework.authtoken.models import Token


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "bio", "profile_picture", "followers"]
        read_only_fields = ["id", "followers"]


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ["username", "email", "password", "first_name", "last_name", "bio"]

    def create(self, validated_data):
        # Use the model manager's create_user to ensure password handling and any custom logic
        password = validated_data.pop("password")
        user = get_user_model().objects.create_user(password=password, **validated_data)
        # create token for the user
        Token.objects.create(user=user)
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data.get("username"), password=data.get("password"))
        if not user:
            raise serializers.ValidationError("Invalid credentials")
        data["user"] = user
        return data
