from django.http import HttpResponse
from django.shortcuts import render


def links(request):
    return HttpResponse('links')
