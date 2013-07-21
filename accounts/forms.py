#! -*- coding:utf-8 -*-
from django import forms


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
    username = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'input-xxlarge',
                'placeholder': u'用户名',
            }
        )
    )
    phone_number = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'input-xxlarge',
                'placeholder': u'手机(选填)'
            }
        )
    )