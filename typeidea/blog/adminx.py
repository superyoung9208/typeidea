import xadmin
from django.contrib import admin
from django.contrib.admin.models import LogEntry
from django.urls import reverse
from django.utils.html import format_html
from xadmin.filters import RelatedFieldListFilter, manager
from xadmin.layout import Fieldset, Row, Container

from .adminforms import PostAdminForm
from typeidea.base_admin import BaseOwnerAdmin

from .models import Category, Post, Tag


# admin.site.site_header = 'Typeidea'
# admin.site.site_title = 'Typeidea后台管理'
# admin.site.index_title = '欢迎使用Typeider后台管理'


# class CategoryOwnerFilter(admin.SimpleListFilter):
#     """自定义过滤器只展示当前用户分类"""
#     title = '分类过滤器'
#     parameter_name = 'owner_category'
#
#     def lookups(self, request, model_admin):
#         return Category.objects.filter(owner=request.user).values_list('id', 'name')
#
#     def queryset(self, request, queryset):
#         category_id = self.value()
#         if category_id:
#             return queryset.filter(category_id=self.value())
#         return queryset


class PostInline:
    form_layout = (
        Container(
            Row("title", "desc"),
        )
    )
    extra = 1  # 控制额外多几个
    model = Post


@xadmin.sites.register(Category)
class CategoryAdmin(BaseOwnerAdmin):
    """类型管理"""

    inlines = (PostInline,)
    list_display = ('name', 'status', 'is_nav', 'create_time', 'post_count')
    fields = ('name', 'status', 'is_nav')

    def post_count(self, obj):
        return obj.post_set.count()

    post_count.short_description = '文章数量'


@xadmin.sites.register(Tag)
class TagAdmin(BaseOwnerAdmin):
    """标签管理"""
    list_display = ('name', 'status', 'create_time')
    fields = ('name', 'status')


class CategoryOwnerFilter(RelatedFieldListFilter):

    @classmethod
    def test(cls, field, request, params, model, admin_view, field_path):
        return field.name == 'category'

    def __init__(self, field, request, params, model, model_admin, field_path):
        super().__init__(field, request, params, model, model_admin, field_path)
        # 重新获取lookup_choices，根据owner过滤
        self.lookup_choices = Category.objects.filter(owner=request.user).values_list('id', 'name')


manager.register(CategoryOwnerFilter, take_priority=True)


@xadmin.sites.register(Post)
class PostAdmin(BaseOwnerAdmin):
    """文章管理"""
    form = PostAdminForm
    list_display = [
        'title', 'category', 'status', 'owner',
        'create_time', 'operator'
    ]

    list_display_links = []
    list_filter = ['category']
    search_fields = ['title', 'category__name']
    # filter_horizontal = ('tag',)  # 多对多字段横向
    filter_vertical = ('tag',)
    actions_on_top = True
    actions_on_bottom = True

    # 编辑页面
    save_on_top = True

    form_layout = (
        Fieldset(
            '基础信息',
            Row("title", "category"),
            'status',
            'tag',
        ),
        Fieldset(
            '内容信息',
            'desc',
            'is_md',
            'content_ck',
            'content_md',
            'content',


        )
    )

    # fieldsets = (
    #     ('基础配置', {
    #         'description': '基础配置描述',
    #         'fields': (
    #             ('title', 'category'),
    #             'status'
    #         )
    #     }),
    #     ('内容', {
    #         'fields': (
    #             'desc',
    #             'content'
    #         )
    #     }),
    #     ('额外信息', {
    #         'classes': ('collapse',),
    #         'fields': ('tag',)
    #     })
    # )

    # class Media:
    #     css = {
    #         'all': ("https://cdn.bootcss.com/bootstrap/4.0 0-beta.2/js/css/bootstrap.min.css",),
    #     }
    #     js = ('https://cdn.bootcss.com/bootstrap/4.0 0-beta.2/js/bootstrap.bundle.js',)




    def operator(self, obj):
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('xadmin:blog_post_change', args=(obj.id,))
        )

    operator.short_description = '操作'

    # def save_model(self, request, obj, form, change):
    #     obj.owner = request.user
    #     return super(PostAdmin, self).save_model(request, obj, form, change)
    #
    # def get_queryset(self, request):
    #     qs = super(PostAdmin, self).get_queryset(request)
    #     return qs.filter(owner=request.user)

# @xadmin.sites.register(LogEntry)
# class LogEntryAdmin(admin.ModelAdmin):
#     list_display = ['object_repr', 'object_id', 'action_flag', 'user', 'change_message']
