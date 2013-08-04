#! -*- coding:utf-8 -*-
from django import forms
from User.models import MyUser


class UserInfo(forms.ModelForm):
    """
    ``个人资料``
    sign  签名
    job 工作
    first_name 名
    last_name 姓
    sex   性别
    birthday  生日
    country   国家
    state     州省
    city      区县
    qq      qq号码
    weibo   微博帐号
    phone_number  电话号码
    """
    sign = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': ''
            }
        )
    )
    job = forms.CharField(
        widget=forms.ChoiceField(
            attrs={
                'class': ''
            }
        )
    )
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': ''
            }
        )
    )
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': ''
            }
        )
    )
    sex = forms.CharField(
        widget=forms.ChoiceField(

        )
    )
    birthday = forms.DateField(
        widget=forms.TextInput(
            attrs={
                'class': ''
            }
        )
    )
    country = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': ''
            }
        )
    )
    state = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': ''
            }
        )
    )
    city = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': ''
            }
        )
    )
    qq = forms.IntegerField(
        widget=forms.TextInput(
            attrs={
                'class': ''
            }
        )
    )
    weibo = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': ''
            }
        )
    )
    phone_number = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': ''
            }
        )
    )