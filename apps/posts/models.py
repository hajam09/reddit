from django.contrib.auth.models import User
from django.db import models

from apps.communities.models import Community, CommunityFlair
from apps.core.models import TimeStampedModel


class Post(TimeStampedModel):
    class Status(models.TextChoices):
        DRAFT = 'DRAFT'
        PUBLIC = 'PUBLIC'
        ARCHIVED = 'ARCHIVED'

    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name='communityPosts')
    title = models.CharField(max_length=512)
    url = models.CharField(max_length=1024)
    content = models.TextField(blank=False)
    creator = models.ForeignKey(User, related_name='postCreator', on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='postLikes')
    dislikes = models.ManyToManyField(User, related_name='postDislikes')
    followers = models.ManyToManyField(User, related_name='postFollowers')
    bookmark = models.ManyToManyField(User, related_name='postBookmarks')
    flair = models.ForeignKey(CommunityFlair, null=True, on_delete=models.SET_NULL, related_name='flairPosts')
