#! -*- coding:utf-8 -*-

from django import forms
from django.forms import ModelForm

from groups.models import Category,Group


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
    create_time     创建时间
    place   群组地点
    flag    区别某些特别群组的标志,初始化时会被赋值
    """
    GROUP_TYPE_CHOICES = (('open', 'Open'), ('private', 'Private'))
    MEMBER_JOIN_CHOICES = (('everyone_can_join', 'Everyone can join'), ('need_check', 'Need check'))
    name = forms.CharField(label=u'名称', widget=forms.TextInput(attrs={}))
    category = forms.ModelChoiceField(label=u'分类', queryset=Category.objects.all(), widget=forms.Select())
    group_type = forms.ChoiceField(label=u'小组类型', choices=GROUP_TYPE_CHOICES, widget=forms.Select(), initial='open')
    member_join = forms.ChoiceField(label=u'加入方式', choices=MEMBER_JOIN_CHOICES, widget=forms.Select(),
                                    initial='everyone_can_join')
    place = forms.CharField(label=u'群组地点', widget=forms.TextInput(attrs={}))

    class Meta:
        model = Group

    def __unicode__(self):
        return "小组:%s" % self.name