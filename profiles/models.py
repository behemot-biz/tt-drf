from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User

"""
Models for the Profiles app.

This module defines the Profile model, which represents a user's profile
information. Each Profile is associated with a User instance and includes
fields for storing additional details such as the user's name, bio content,
and profile image.

A signal is included to automatically create a Profile when a new User is
registered.

Classes:
    - Profile: Represents a user's profile with additional metadata.

Functions:
    - create_profile: Signal handler to create a Profile when a new User is
      registered.
"""


class Profile(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255, blank=True)
    content = models.TextField(blank=True)
    image = models.ImageField(
        upload_to='images/', default='../default_profile_rws25d'
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.owner}'s profile"


def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(owner=instance)


post_save.connect(create_profile, sender=User)
