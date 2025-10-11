from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User
from .serializers import UserSerializer, RegisterSerializer, LoginSerializer


class RegisterView(generics.CreateAPIView):
	queryset = User.objects.all()
	serializer_class = RegisterSerializer
	permission_classes = [permissions.AllowAny]

	def create(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		user = serializer.save()
		token, _ = Token.objects.get_or_create(user=user)
		data = UserSerializer(user, context={"request": request}).data
		data["token"] = token.key
		return Response(data, status=status.HTTP_201_CREATED)


class LoginView(APIView):
	permission_classes = [permissions.AllowAny]

	def post(self, request):
		serializer = LoginSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		user = serializer.validated_data["user"]
		token, _ = Token.objects.get_or_create(user=user)
		data = UserSerializer(user, context={"request": request}).data
		data["token"] = token.key
		return Response(data)


class ProfileView(generics.RetrieveUpdateAPIView):
	serializer_class = UserSerializer
	permission_classes = [permissions.IsAuthenticated]

	def get_object(self):
		return get_object_or_404(User, pk=self.request.user.pk)


class FollowToggleView(APIView):
	permission_classes = [permissions.IsAuthenticated]

	def post(self, request, user_id):
		# follow the user with id=user_id
		target = get_object_or_404(User, pk=user_id)
		if target == request.user:
			return Response({"detail": "Cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)
		request.user.following.add(target)
		return Response({"detail": f"Now following {target.username}"})

	def delete(self, request, user_id):
		# unfollow the user with id=user_id
		target = get_object_or_404(User, pk=user_id)
		if target == request.user:
			return Response({"detail": "Cannot unfollow yourself."}, status=status.HTTP_400_BAD_REQUEST)
		request.user.following.remove(target)
		return Response({"detail": f"Unfollowed {target.username}"})

