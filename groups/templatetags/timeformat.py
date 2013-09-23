#coding=utf-8
import datetime
from django import template
from django.utils import timezone
register = template.Library()


@register.filter
def timeformat(date):
    if type(date) is float:
        date = datetime.datetime.fromtimestamp(date)
    end = timezone.now()
    delta = end - date
    days = delta.days
    seconds = delta.seconds
    if days >= 2:
        return date
    if days > 0:
        return u"%d天前" % days
    if seconds > 3600:
        hours = int(seconds / 3600)
        return u"%d个小时前" % hours
    if seconds > 60:
        minutes = int(seconds / 60)
        return u"%d分钟前" % minutes
    return u"1分钟前"