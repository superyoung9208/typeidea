from django.contrib import admin
from django.contrib.admin.models import LogEntry
from django.urls import reverse
from django.utils.html import format_html
from .adminforms import PostAdminForm
from typeidea.custom_site import custom_site
from typeidea.base_admin import BaseOwnerAdmin

from .models import Category, Post, Tag

admin.site.site_header = 'Typeidea'
admin.site.site_title = 'Typeidea后台管理'
admin.site.index_title = '欢迎使用Typeider后台管理'


class CategoryOwnerFilter(admin.SimpleListFilter):
    """自定义过滤器只展示当前用户分类"""
    title = '分类过滤器'
    parameter_name = 'owner_category'

    def lookups(self, request, model_admin):
        return Category.objects.filter(owner=request.user).values_list('id', 'name')

    def queryset(self, request, queryset):
        category_id = self.value()
        if category_id:
            return queryset.filter(category_id=self.value())
        return queryset


class PostInline(admin.TabularInline):
    fields = ('title', 'desc')
    extra = 1
    model = Post


@admin.register(Category)
class CategoryAdmin(BaseOwnerAdmin):
    """类型管理"""

    inlines = (PostInline,)
    list_display = ('name', 'status', 'is_nav', 'create_time', 'post_count')
    fields = ('name', 'status', 'is_nav')

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(CategoryAdmin, self).save_model(request, obj, form, change)

    def post_count(self, obj):
        return obj.post_set.count()

    post_count.short_description = '文章数量'


@admin.register(Tag)
class TagAdmin(BaseOwnerAdmin):
    """标签管理"""
    list_display = ('name', 'status', 'create_time')
    fields = ('name', 'status')

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(TagAdmin, self).save_model(request, obj, form, change)


@admin.register(Post)
class PostAdmin(BaseOwnerAdmin):
    """文章管理"""
    form = PostAdminForm
    list_display = [
        'title', 'category', 'status', 'owner',
        'create_time', 'operator'
    ]

    list_display_links = []
    list_filter = [CategoryOwnerFilter]
    search_fields = ['title', 'category__name']
    # filter_horizontal = ('tag',)  # 多对多字段横向
    filter_vertical = ('tag',)
    actions_on_top = True
    actions_on_bottom = True

    # 编辑页面
    save_on_top = True

    # fields = (
    #     ('category', 'title'),
    #     'desc',
    #     'status',
    #     'context',
    #     'tag'
    # )

    fieldsets = (
        ('基础配置', {
            'description': '基础配置描述',
            'fields': (
                ('title', 'category'),
                'status'
            )
        }),
        ('内容', {
            'fields': (
                'desc',
                'context'
            )
        }),
        ('额外信息', {
            'classes': ('collapse',),
            'fields': ('tag',)
        })
    )

    class Media:
        css = {
            'all': ("https://cdn.bootcss.com/bootstrap/4.0 0-beta.2/js/css/bootstrap.min.css",),
        }
        js = ('https://cdn.bootcss.com/bootstrap/4.0 0-beta.2/js/bootstrap.bundle.js',)

    def operator(self, obj):
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('admin:blog_post_change', args=(obj.id,))
        )

    operator.short_description = '操作'

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(PostAdmin, self).save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super(PostAdmin, self).get_queryset(request)
        return qs.filter(owner=request.user)


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ['object_repr', 'object_id', 'action_flag', 'user', 'change_message']
