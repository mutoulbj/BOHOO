#! -*- coding:utf-8 -*-
from django import forms
from django.forms.extras import SelectDateWidget

from User.models import MyUser

from User.utils import get_last_70_year_range


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
        required=False,
        widget=forms.Textarea(
            attrs={
                'class': 'span11',
                'rows': '4',
            }
        )
    )
    job = forms.CharField(
        label=u'职业',
        required=False,
        widget=forms.Select(
            choices=(("", "---"),),
            attrs={
                'class': 'span10'
            }
        )
    )
    first_name = forms.CharField(
        label=u'名',
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'span10'
            }
        )
    )
    last_name = forms.CharField(
        label=u'姓',
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'span10'
            }
        )
    )
    sex = forms.ChoiceField(
        label=u'性别',
        required=False,
        choices=SEX_CHOICES,
        widget=forms.RadioSelect(
            attrs={
                'class': 'text-info'
            }
        )
    )
    birthday = forms.DateTimeField(
        label=u'生日',
        required=False,
        widget=SelectDateWidget(
            years=get_last_70_year_range(),
            attrs={
                'class': 'span10'
            }
        )
    )
    country = forms.CharField(
        label=u'国家',
        required=False,
        widget=forms.Select(
            choices=(("", "---"),),
            attrs={
                'class': 'input-small'
            }
        )
    )
    state = forms.CharField(
        label=u'州省',
        required=False,
        widget=forms.Select(
            choices=(("", "---"),),
            attrs={
                'class': 'input-small'
            }
        )
    )
    city = forms.CharField(
        label=u'市县',
        required=False,
        widget=forms.Select(
            choices=(("", "---"),),
            attrs={
                'class': 'input-small'
            }
        )
    )
    qq = forms.IntegerField(
        label=u'QQ',
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'span10'
            }
        )
    )
    weibo = forms.CharField(
        label=u'微博',
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'span10'
            }
        )
    )
    phone_number = forms.CharField(
        label=u'手机号码',
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'span10'
            }
        )
    )

    class Meta:
        model = MyUser
        fields = ('sign', 'job', 'first_name', 'last_name', 'sex', 'birthday', 'country', 'state', 'city', 'qq',
                  'weibo', 'phone_number')