from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView

from blog.views import CommonViewMixin
from config.models import Link


class LinkListView(CommonViewMixin, ListView):
    """友链页面"""
    queryset = Link.objects.filter(status=Link.STATUS_NORMAL)
    template_name = 'config/links.html'
    context_object_name = 'link_list'

