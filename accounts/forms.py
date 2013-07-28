#! -*- coding:utf-8 -*-
from django import forms
from django.core.exceptions import ObjectDoesNotExist
from User.models import MyUser


class login_form(forms.Form):
    """
    登录
    """
    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={
                'placeholder': u'邮件',
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': u'密码',
            }
        )
    )


class register_form(forms.Form):
    """
    注册
    """
    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={
                'class': 'input-xxlarge',
                'placeholder': u'邮件',
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'input-xxlarge',
                'placeholder': u'密码',
            }
        )
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'input-xxlarge',
                'placeholder': u'重复密码',
            }
        )
    )
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'input-xxlarge',
                'placeholder': u'用户名',
            }
        )
    )
    phone_number = forms.IntegerField(
        # required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'input-xxlarge',
                'placeholder': u'手机(选填)'
            }
        )
    )

    def clean_password1(self):
        data = self.cleaned_data
        password = data['password']
        password1 = data['password1']
        if password == password1:
            return password1
        raise forms.ValidationError(u'密码必须一致')

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            MyUser.objects.get(username=username)
        except ObjectDoesNotExist:
            return username
        raise forms.ValidationError(u'该用户名已经存在')

    def save(self):
        data = self.cleaned_data
        MyUser.objects.create_user(email=data['email'], username=data['username'], password=data['password'])
