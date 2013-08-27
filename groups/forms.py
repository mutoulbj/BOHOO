#! -*- coding:utf-8 -*-

from django import forms
from django.forms import ModelForm

from groups.models import Category, Group


class category(ModelForm):
    """ 分类form @fanlintao
    name    分类名称
    parent  父分类
    """
    name = forms.CharField(label=u'名称', widget=forms.TextInput(attrs={}))
    parent = forms.ModelChoiceField(label=u'父分类', queryset=Category.objects.all(), widget=forms.Select())

    class Meta:
        model = Category

    def __unicode__(self):
        return "分类:%s" % self.name


class group(ModelForm):
    """ 小组form @fanlintao
    name            名称
    description     描述
    category        分类
    group_type      小组类型
    member_join     加入小组的方式
    place   群组地点
    """
    GROUP_TYPE_CHOICES = (('open', u'公开'), ('private', u'秘密'))
    MEMBER_JOIN_CHOICES = (('everyone_can_join', '任何人'), ('need_check', '需要验证'))

    name = forms.CharField(label=u'名称',
                           widget=forms.TextInput(
                               attrs={'class': 'span10 required', 'placeholder': u'小组的名称'}
                           ))
    category = forms.ModelChoiceField(label=u'分类', queryset=Category.objects.all(),
                                      widget=forms.Select(attrs={'class': 'span4 required'}))
    group_type = forms.ChoiceField(label=u'小组类型', choices=GROUP_TYPE_CHOICES,
                                   widget=forms.Select(attrs={'class': 'span4 required'}), initial='open')
    member_join = forms.ChoiceField(label=u'加入方式', choices=MEMBER_JOIN_CHOICES,
                                    widget=forms.Select(attrs={'class': 'span4 required'}),
                                    initial='everyone_can_join')
    place = forms.CharField(label=u'群组地点',
                            widget=forms.TextInput(attrs={'class': 'span10 required', 'placeholder': u'群组的根据地'}))
    description = forms.CharField(label=u'描述',
                                  widget=forms.Textarea(
                                      attrs={'class': 'span10 required', 'placeholder': u'群组作用、功能等简要描述'}
                                  ))

    class Meta:
        model = Group
        fields = ('name', 'category', 'group_type', 'member_join', 'place', 'description')

    def __unicode__(self):
        return "小组:%s" % self.name