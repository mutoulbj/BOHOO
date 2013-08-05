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
    # TODO : 未完成
    SEX_CHOICES = (('M', u'男'), ('F', u'女'))
    sign = forms.CharField(
        label=u'签名',
        widget=forms.Textarea(
            attrs={
                'class': 'input-medium'
            }
        )
    )
    job = forms.ChoiceField(
        label=u'职业',
        widget=forms.Select(
            # attrs={
            #     'class': ''
            # }
        )
    )
    first_name = forms.CharField(
        label=u'名',
        widget=forms.TextInput(
            attrs={
                'class': 'input-medium'
            }
        )
    )
    last_name = forms.CharField(
        label=u'姓',
        widget=forms.TextInput(
            attrs={
                'class': 'input-medium'
            }
        )
    )
    sex = forms.ChoiceField(
        label=u'性别',
        choices=SEX_CHOICES,
        widget=forms.RadioSelect(

        )
    )
    birthday = forms.DateField(
        label=u'生日',
        widget=forms.DateInput(
            attrs={
                'class': ''
            }
        )
    )
    country = forms.CharField(
        label=u'国家',
        widget=forms.TextInput(
            attrs={
                'class': ''
            }
        )
    )
    state = forms.CharField(
        label=u'州省',
        widget=forms.TextInput(
            attrs={
                'class': ''
            }
        )
    )
    city = forms.CharField(
        label=u'市县',
        widget=forms.TextInput(
            attrs={
                'class': ''
            }
        )
    )
    qq = forms.IntegerField(
        label=u'QQ',
        widget=forms.TextInput(
            attrs={
                'class': 'input-medium'
            }
        )
    )
    weibo = forms.CharField(
        label=u'微博',
        widget=forms.TextInput(
            attrs={
                'class': 'input-medium'
            }
        )
    )
    phone_number = forms.CharField(
        label=u'手机号码',
        widget=forms.TextInput(
            attrs={
                'class': 'input-medium'
            }
        )
    )

    class Meta:
        model = MyUser