from django.contrib.auth.models import AbstractUser
from django.db import models
from .managers import CustomUserManager


class CustomUser(AbstractUser):
    """
    Custom user model extending Django's AbstractUser.
    Adds additional fields: date_of_birth and profile_photo.
    """
    date_of_birth = models.DateField(
        null=True, 
        blank=True,
        help_text="User's date of birth"
    )
    profile_photo = models.ImageField(
        upload_to='profile_photos/',
        null=True,
        blank=True,
        help_text="User's profile photo"
    )
    
    objects = CustomUserManager()
    
    def __str__(self):
        return self.username