from django.contrib.auth.models import User
from django.db import models

from apps.core.models import TimeStampedModel
from apps.posts.models import Post


class AbstractReport(TimeStampedModel):
    class Status(models.TextChoices):
        INITIATED = 'INITIATED', 'Initiated'
        VERIFIED = 'VERIFIED', 'Verified'
        RESOLVED = 'RESOLVED', 'Resolved'
        REJECTED = 'REJECTED', 'Rejected'
        REDACTED = 'REDACTED', 'Redacted'
        PENDING = 'PENDING', 'Pending'

    reporter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reporters%(class)s')
    title = models.CharField(max_length=256)
    details = models.TextField(blank=True)
    status = models.CharField(
        choices=Status.choices,
        max_length=16,
        default=Status.INITIATED,
        help_text='''
            1. Initiated: Anyone can create a report. Does not mean it is valid.<br>
            2. Verified: Report is valid and further actions can be taken.<br>
            3. Resolved: The Report was verified but is no longer valid. The problem has been solved.<br>
            4. Rejected: Verified and found the report has no basis. Fake/Invalid.<br>
            5. Redacted: User is withdrawing the report.<br>
            6. Pending: Awaiting further action.
        '''
    )

    class Meta:
        abstract = True


class PostReport(AbstractReport):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='postReports')

    def __str__(self):
        return f'Report: {self.post.title} by {self.reporter.username}'


class UserReport(AbstractReport):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='userReports')

    def __str__(self):
        return f'Report: {self.user.username} by {self.reporter.username}'
