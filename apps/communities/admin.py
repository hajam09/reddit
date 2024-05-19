from django.contrib import admin

from apps.communities.models import (
    Community,
    CommunityMember,
    CommunityInvite,
    CommunityMemberRequest,
    CommunityPage,
    CommunityRule,
    CommunityFlair
)

admin.site.register(Community)
admin.site.register(CommunityMember)
admin.site.register(CommunityInvite)
admin.site.register(CommunityMemberRequest)
admin.site.register(CommunityPage)
admin.site.register(CommunityRule)
admin.site.register(CommunityFlair)
