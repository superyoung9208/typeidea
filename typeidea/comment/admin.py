from django.contrib import admin
from typeidea.base_admin import BaseOwnerAdmin

from comment.models import Comment


@admin.register(Comment)
class CommentAdmin(BaseOwnerAdmin):
    list_display = ('target', 'nick_name', 'content', 'website', 'create_time')
