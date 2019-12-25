import xadmin
from django.contrib import admin
from typeidea.base_admin import BaseOwnerAdmin
from config.models import Link, Sidebar


@xadmin.sites.register(Link)
class LinkAdmin(BaseOwnerAdmin):
    list_display = ('title', 'href', 'status', 'weight', 'create_time')
    fields = ('title', 'href', 'status', 'weight')

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(LinkAdmin, self).save_model(request, obj, form, change)


@xadmin.sites.register(Sidebar)
class SidebarAdmin(BaseOwnerAdmin):
    list_display = ('title', 'display_type', 'content', 'create_time')
    fields = ('title', 'display_type', 'content')

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(SidebarAdmin, self).save_model(request, obj, form, change)
