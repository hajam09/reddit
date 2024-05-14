from colorfield.fields import ColorField
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.db import models


class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    edited = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.pk is not None:
            self.edited = True
        super(TimeStampedModel, self).save(*args, **kwargs)

    class Meta:
        abstract = True


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


class Community(TimeStampedModel):
    class Type(models.TextChoices):
        PUBLIC = 'PUBLIC'
        RESTRICTED = 'RESTRICTED'
        PRIVATE = 'PRIVATE'

    name = models.CharField(max_length=32, unique=True)
    header = models.CharField(max_length=256, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    banner = models.ImageField(upload_to='community-banner/', blank=True, null=True)
    logo = models.ImageField(upload_to='community-logo/', blank=True, null=True)
    relatedCommunities = ArrayField(models.CharField(max_length=8192), blank=True)
    communityType = models.CharField(
        choices=Type.choices,
        max_length=16,
        default=Type.PUBLIC,
        help_text='''
            <b>PUBLIC</b>: Anyone can view, post, and comment to this community.<br>
            <b>RESTRICTED</b>: Anyone can view this community, but only approved users can post.<br>
            <b>PRIVATE</b>: Only approved users can view and submit to this community.
        '''
    )
    archivePosts = models.BooleanField(
        default=False,
        help_text='Posts after a period of X months will be archived automatically'
    )

    @property
    def admins(self):
        return self.communityMembers.filter(memberType=CommunityMember.MemberTypes.ADMIN)

    @property
    def moderators(self):
        return self.communityMembers.filter(memberType=CommunityMember.MemberTypes.MODERATOR)

    @property
    def members(self):
        return self.communityMembers.filter(memberType=CommunityMember.MemberTypes.MEMBER)


class CommunityMember(TimeStampedModel):
    class MemberTypes(models.TextChoices):
        ADMIN = 'ADMIN'
        MODERATOR = 'MODERATOR'
        MEMBER = 'MEMBER'

    class Status(models.TextChoices):
        ACTIVE = 'ACTIVE'
        BANNED = 'BANNED'
        MUTED = 'MUTED'

    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name='communityMembers')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='communityUsers')
    memberType = models.CharField(
        choices=MemberTypes.choices,
        max_length=16,
        default=MemberTypes.MEMBER,
        help_text=''' 
            <b>ADMIN</b>: Has (all) permissions to add or remove members as moderators, ban or mute members.<br>
            <b>MODERATOR</b>: Has permission to add, remove, ban or mute members.<br>
            <b>MEMBER</b>: Can post, like, comment, share, bookmark group posts.
        '''
    )
    status = models.CharField(
        choices=Status.choices,
        max_length=16,
        default=Status.ACTIVE,
        help_text=''' 
            <b>ACTIVE</b>: Can be active in a group within permissions.<br>
            <b>MUTED</b>: Forbidden for any activity (post, comment etc.) in a group for a week.<br>
            <b>BANNED</b>: Forbidden for any activity in a group forever.
        '''
    )

    def __str__(self):
        return f'{self.user.username} added to {self.community.name} as {self.memberType}'


class CommunityInvite(TimeStampedModel):
    class InviteAs(models.TextChoices):
        MEMBER = 'MEMBER'
        MODERATOR = 'MODERATOR'

    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name='communityInvites')
    inviter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='communityInviter')
    invitee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='communityInvitee')
    inviteAs = models.CharField(choices=InviteAs.choices, default=InviteAs.MEMBER, max_length=16)

    def __str__(self):
        return f'{self.inviter.username} has invited {self.invitee.username} to join {self.community.name} as {self.inviteAs}'


class CommunityMemberRequest(TimeStampedModel):
    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name='communityMemberRequests')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='communityMemberRequestedUser')
    isApproved = models.BooleanField(default=False)


class CommunityPage(TimeStampedModel):
    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name='communityPages')
    title = models.CharField(max_length=16)
    content = models.TextField()


class CommunityRule(TimeStampedModel):
    class RuleType(models.TextChoices):
        POSTS = 'POSTS'
        COMMENTS = 'COMMENTS'
        BOTH = 'BOTH'

    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name='communityRules')
    title = models.CharField(max_length=512)
    description = models.TextField()
    ruleType = models.CharField(choices=RuleType.choices, max_length=10, default=RuleType.BOTH)


class CommunityFlair(TimeStampedModel):
    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name='communityFlares')
    name = models.CharField(max_length=512)
    color = ColorField(default='#FF0000')


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
