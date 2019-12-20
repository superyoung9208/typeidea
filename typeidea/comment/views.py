from django.shortcuts import render, redirect

# Create your views here.
from django.views.generic import TemplateView

from comment.forms import CommentForm


class CommentView(TemplateView):
    http_method_names = ['post']
    template_name = 'comment/result.html'

    def post(self, request, *args, **kwargs):
        """提交评论"""
        comment_form = CommentForm(request.POST)
        target = request.POST.get('target')

        if comment_form.is_valid():
            instance = comment_form.save(commit=False)
            instance.target = target
            instance.save()
            success = True
            return redirect(target)
        else:
            success = False

        context = {
            'success': success,
            'form': comment_form,
            'target': target
        }

        return self.render_to_response(context)
