from django.contrib import admin

from apps.reports.models import (
    PostReport,
    UserReport
)

admin.site.register(PostReport)
admin.site.register(UserReport)
