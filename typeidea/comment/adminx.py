from django.contrib import admin
from typeidea.base_admin import BaseOwnerAdmin
import xadmin
from comment.models import Comment


@xadmin.sites.register(Comment)
class CommentAdmin:
    list_display = ('target', 'nick_name', 'content', 'website', 'create_time')
