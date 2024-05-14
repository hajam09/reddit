from django.contrib import admin

from core.models import (
    Profile,
    Community,
    CommunityMember,
    CommunityInvite,
    CommunityMemberRequest,
    CommunityPage,
    CommunityRule,
    CommunityFlair,
    Post,
    PostComment,
    PostReport,
    UserReport
)

admin.site.register(Profile)
admin.site.register(Community)
admin.site.register(CommunityMember)
admin.site.register(CommunityInvite)
admin.site.register(CommunityMemberRequest)
admin.site.register(CommunityPage)
admin.site.register(CommunityRule)
admin.site.register(CommunityFlair)
admin.site.register(Post)
admin.site.register(PostComment)
admin.site.register(PostReport)
admin.site.register(UserReport)
