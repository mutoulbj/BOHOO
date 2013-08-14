#! -*- coding:utf-8 -*-
from django import template

from friends.models import FriendShip

register = template.Library()

@register.filter
def following(curuser, user):
    """
    {% if curuser|following:user %}
    curuser is following user
    {% else %}
    curuser is not following user
    {% endif %}
    """
    return FriendShip.objects.filter(from_user = curuser, to_user = user).exists()

@register.filter
def followed(curuser, user):
    """
    {% if curuser|following:user %}
    curuser is followed user
    {% else %}
    curuser is not followed user
    {% endif %}
    """
    return FriendShip.objects.filter(to_user = curuser, from_user = user).exists()