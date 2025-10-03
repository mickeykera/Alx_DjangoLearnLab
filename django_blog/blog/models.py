from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from django.conf import settings
from django.db.models.signals import post_save


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    tags = TaggableManager()

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("post-detail", kwargs={"pk": self.pk})


class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"Comment by {self.author.username} on {self.post.title}"


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_pics/', default='profile_pics/default.jpg', blank=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username} Profile"

# Signal to create or update Profile after User is saved
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()

post_save.connect(create_or_update_user_profile, sender=settings.AUTH_USER_MODEL)
