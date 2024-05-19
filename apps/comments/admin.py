from django.contrib import admin

from apps.comments.models import (
    PostComment
)

admin.site.register(PostComment)
