from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import PostViewSet, CommentViewSet, FeedView, LikePostView, UnlikePostView

router = DefaultRouter()
router.register(r"posts", PostViewSet, basename="post")
router.register(r"comments", CommentViewSet, basename="comment")

urlpatterns = router.urls + [
	path("feed/", FeedView.as_view(), name="feed"),
	path("posts/<int:pk>/like/", LikePostView.as_view(), name="post-like"),
	path("posts/<int:pk>/unlike/", UnlikePostView.as_view(), name="post-unlike"),
]
