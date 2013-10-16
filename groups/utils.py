#! -*- coding:utf-8 -*-

from groups.models import Group


def get_groups(user):
    """ 根据用户返回其参加的所有群组 """
    return Group.objects.filter(member=user)


def get_most_topic_groups(user, n=1):
    """
    返回用户所在职业下话题最多的n个群组,默认为1
    返回queryset
    """
    return Group.objects.filter(category__name=user.job).order_by('-topic_amount')[0:n]


