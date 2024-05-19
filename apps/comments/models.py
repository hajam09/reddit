from django.contrib.auth.models import User
from django.db import models

from apps.core.models import TimeStampedModel
from apps.posts.models import Post


class PostComment(TimeStampedModel):
    post = models.ForeignKey(Post, related_name='postComments', on_delete=models.CASCADE)
    parent = models.ForeignKey('self', null=True, on_delete=models.CASCADE, related_name='parentComments')
    likes = models.ManyToManyField(User, related_name='postCommentLikes', blank=True)
    dislikes = models.ManyToManyField(User, related_name='postCommentDislikes', blank=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='creatorPostComments')
    _comment = models.TextField()
    isRemoved = models.BooleanField(
        default=False,
        help_text='''
            Check this box if the comment is inappropriate.<br>
            A "This comment has been removed" message will be displayed instead.
        '''
    )
    isNestingPermitted = models.BooleanField(default=False)
    mentionedUsers = models.ManyToManyField(User, blank=True, related_name='postCommentMentionedUsers')

    @property
    def comment(self):
        if self.isRemoved:
            return 'This comment has been removed.'
        return self._comment

    @comment.setter
    def comment(self, value):
        self._comment = value
