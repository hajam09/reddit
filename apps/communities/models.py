from colorfield.fields import ColorField
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.db import models

from apps.core.models import TimeStampedModel


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
