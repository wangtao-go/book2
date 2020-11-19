from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError

import app01.models


class VideoPublishForm(forms.ModelForm):
    title = forms.CharField(min_length=4, max_length=200, required=True,
                            error_messages={
                                'min_length': '至少4个字符',
                                'max_length': '不能多于200个字符',
                                'required': '标题不能为空'
                            },
                            widget=forms.TextInput(attrs={'placeholder': '请输入内容'}))
    desc = forms.CharField(min_length=4, max_length=200, required=True,
                           error_messages={
                               'min_length': '至少4个字符',
                               'max_length': '不能多于200个字符',
                               'required': '描述不能为空'
                           },
                           widget=forms.Textarea(attrs={'placeholder': '请输入内容'}))
    cover = forms.ImageField(required=True,
                             error_messages={
                                 'required': '封面不能为空'
                             },
                             widget=forms.FileInput(attrs={'class': 'n'}))
    status = forms.CharField(min_length=1, max_length=1, required=False,
                             widget=forms.HiddenInput(attrs={'value': '0'}))

    class Meta:
        model = app01.models.Video
        fields = ['title', 'desc', 'status', 'cover']
