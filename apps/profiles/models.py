from django.contrib.auth.models import User
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.db import models

from apps.core.models import TimeStampedModel


class Profile(TimeStampedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', unique=True, db_index=True)
    displayName = models.CharField(max_length=512, blank=True, null=True)
    about = models.TextField(blank=True, null=True)
    dateOfBirth = models.DateField(blank=True, null=True)
    dateOfBirthVisible = models.BooleanField(default=False)
    favouriteCommunities = ArrayField(models.CharField(max_length=8192), blank=True)
    mutedCommunities = ArrayField(models.CharField(max_length=8192), blank=True)
    avatar = models.ImageField(upload_to='profile-avatar', blank=True, null=True)
    banner = models.ImageField(upload_to='profile-banner', blank=True, null=True)
    isBanned = models.DateField(blank=True, null=True)
    isRequestingDelete = models.BooleanField(default=False)
    followers = models.ManyToManyField(User, related_name='userFollowers')
