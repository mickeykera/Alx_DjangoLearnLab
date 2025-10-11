from django.urls import path

from .views import RegisterView, LoginView, ProfileView, FollowToggleView, UserListView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("follow/<int:user_id>/", FollowToggleView.as_view(), name="follow-toggle"),
    path("unfollow/<int:user_id>/", FollowToggleView.as_view(), name="unfollow-toggle"),
    path("users/", UserListView.as_view(), name="user-list"),
]
