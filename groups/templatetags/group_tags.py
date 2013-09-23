#! -*- coding:utf-8 -*-
from django import template
register = template.Library()


@register.simple_tag()
def get_group_type(group_type):
    if group_type == 'open':
        return u'公开'
    elif group_type == 'private':
        return u'秘密'
