from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
	"""
	Custom User model extending AbstractUser.

	Fields added:
	- bio: optional text field
	- profile_picture: optional image upload
	- followers: ManyToMany to self (symmetrical=False) representing users who follow this user
	"""

	bio = models.TextField(blank=True, null=True)
	profile_picture = models.ImageField(upload_to="profiles/", blank=True, null=True)
	followers = models.ManyToManyField(
		"self", symmetrical=False, related_name="following", blank=True
	)

	def __str__(self):
		return self.username
