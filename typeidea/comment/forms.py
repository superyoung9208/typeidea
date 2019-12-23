"""
File:comment/forms.py
Author:PeterYoung
Description:提供表单
"""
from django import forms
from .models import Comment
import mistune


class CommentForm(forms.ModelForm):
    """提交评论的表单"""
    nick_name = forms.CharField(
        label='昵称',
        max_length=50,
        widget=forms.widgets.Input(
            attrs={'class': 'form-control', 'style': 'width: 60%;'}
        )
    )
    email = forms.CharField(
        label='Email',
        max_length=50,
        widget=forms.widgets.EmailInput(
            attrs={'class': 'form-control', 'style': 'width: 60%;'}
        )
    )
    website = forms.CharField(
        label='网站',
        max_length=100,
        widget=forms.widgets.URLInput(
            attrs={'class': 'form-control', 'style': 'width: 60%;'}
        )
    )

    content = forms.CharField(
        label='内容',
        max_length=500,
        widget=forms.widgets.Textarea(
            attrs={'class': 'form-control', 'style': 'width: 60%;'}
        )
    )

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if len(content) < 10:
            raise forms.ValidationError('内容长度怎么这么短呢!!')
        content = mistune.markdown(content)  # markdown格式转换为html格式
        return content

    class Meta:
        model = Comment
        fields = ['nick_name', 'email', 'website', 'content']
