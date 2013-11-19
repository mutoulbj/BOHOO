# coding=utf-8
# -*- coding:utf-8 -*-
import json
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.template import loader, RequestContext
from django.shortcuts import redirect, get_object_or_404
from django.utils.datastructures import MultiValueDictKeyError
from Bohoo.settings import JOINED_GROUPS_NUM, ADD_TOPIC_NUM, REPLY_TOPIC_NUM

from User.models import MyUser
from User.forms import UserInfo
from friends.models import Friendship
from groups.models import Topic, Reply

from groups.utils import get_groups


@login_required()
def edit(request):
    """
    编辑个人资料
    @fanlintao
    """
    if request.method == "POST":
        form = UserInfo(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
    vt = loader.get_template("people/edit.html")
    c = RequestContext(
        request, {
            'form': UserInfo(instance=request.user)
        }
    )
    return HttpResponse(vt.render(c))


def view_profile(request, tid):
    """
    查看个人资料
    @fanlintao
    """
    t_user = get_object_or_404(MyUser, id=tid)
    #关注了
    t_followed = Friendship.objects.filter(from_user=t_user)

    # 关注者
    t_follower = Friendship.objects.filter(to_user=t_user)

    vt = loader.get_template("people/profile.html")
    c = RequestContext(
        request, {
            'user': t_user,
            'followed': t_followed,
            'follower': t_follower
        }
    )
    return HttpResponse(vt.render(c))


def view_info(request, tid):
    """
    查看他人资料: 加入的群组
    @fanlintao
    """
    t_user = get_object_or_404(MyUser, id=tid)
    t_joined_groups = get_groups(t_user)[0:JOINED_GROUPS_NUM:-1]   # 加入的群组
    active_tab = 'followed'    # 默认激活'关注了'的tab


    #关注了
    t_followed = Friendship.objects.filter(from_user=t_user)

    # 关注者
    t_follower = Friendship.objects.filter(to_user=t_user)

    try:
        if request.method == 'GET':
            f_user = get_object_or_404(MyUser, id=request.GET['follow_user'])
            t_followed = Friendship.objects.filter(from_user=f_user)
            t_follower = Friendship.objects.filter(to_user=f_user)
            active_tab = request.GET['follow_type']
    except MultiValueDictKeyError:
        pass

    # 是否已经关注
    is_followed = False
    if not request.user.is_anonymous():
        f_list = Friendship.objects.filter(from_user=request.user, to_user=t_user).values_list('from_user', flat=True)
    else:
        f_list = []
    if request.user.id in f_list:
        is_followed = True

    vt = loader.get_template("people/member_info/group_joined.html")
    c = RequestContext(
        request, {
            't_user': t_user,
            'is_followed': is_followed,
            'joined_groups': t_joined_groups,
            'followed': t_followed,
            'follower': t_follower,
            'active_tab': active_tab
        }
    )
    return HttpResponse(vt.render(c))


def m_add_topic(request, tid):
    """
    查看他人资料: 添加的话题
    @fanlintao
    """
    t_user = get_object_or_404(MyUser, id=tid)
    t_add_topic = Topic.objects.filter(creator=t_user).order_by('-create_time')[0:ADD_TOPIC_NUM]   # 添加的话题

    active_tab = 'followed'    # 默认激活'关注了'的tab


    #关注了
    t_followed = Friendship.objects.filter(from_user=t_user)

    # 关注者
    t_follower = Friendship.objects.filter(to_user=t_user)

    try:
        if request.method == 'GET':
            f_user = get_object_or_404(MyUser, id=request.GET['follow_user'])
            t_followed = Friendship.objects.filter(from_user=f_user)
            t_follower = Friendship.objects.filter(to_user=f_user)
            active_tab = request.GET['follow_type']
    except MultiValueDictKeyError:
        pass

    # 是否已经关注
    is_followed = False
    if not request.user.is_anonymous():
        f_list = Friendship.objects.filter(from_user=request.user, to_user=t_user).values_list('from_user', flat=True)
    else:
        f_list = []
    if request.user.id in f_list:
        is_followed = True

    vt = loader.get_template("people/member_info/topic_add.html")
    c = RequestContext(
        request, {
            't_user': t_user,
            'is_followed': is_followed,
            'add_topics': t_add_topic,
            'followed': t_followed,
            'follower': t_follower,
            'active_tab': active_tab
        }
    )
    return HttpResponse(vt.render(c))


def m_reply_topic(request, tid):
    """
    查看他人资料: 回复的话题
    @fanlintao
    """
    t_user = get_object_or_404(MyUser, id=tid)
    t_r_topic_ids = Reply.objects.filter(creator=t_user, reply__isnull=True,
                                         topic__isnull=False).values_list('topic', flat=True)
    t_reply_topics = Topic.objects.filter(id__in=list(set(t_r_topic_ids))).order_by('-create_time')[0:REPLY_TOPIC_NUM]
    active_tab = 'followed'    # 默认激活'关注了'的tab


    #关注了
    t_followed = Friendship.objects.filter(from_user=t_user)

    # 关注者
    t_follower = Friendship.objects.filter(to_user=t_user)

    try:
        if request.method == 'GET':
            f_user = get_object_or_404(MyUser, id=request.GET['follow_user'])
            t_followed = Friendship.objects.filter(from_user=f_user)
            t_follower = Friendship.objects.filter(to_user=f_user)
            active_tab = request.GET['follow_type']
    except MultiValueDictKeyError:
        pass

    # 是否已经关注
    is_followed = False
    if not request.user.is_anonymous():
        f_list = Friendship.objects.filter(from_user=request.user, to_user=t_user).values_list('from_user', flat=True)
    else:
        f_list = []
    if request.user.id in f_list:
        is_followed = True

    vt = loader.get_template("people/member_info/topic_reply.html")
    c = RequestContext(
        request, {
            't_user': t_user,
            'is_followed': is_followed,
            'reply_topics': t_reply_topics,
            'followed': t_followed,
            'follower': t_follower,
            'active_tab': active_tab
        }
    )
    return HttpResponse(vt.render(c))


@login_required()
def base_info_edit(request):
    """
    编辑基本资料
    @fanlintao
    """

    if request.method == "POST":
        form = UserInfo(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect(reverse('index'))
    vt = loader.get_template("people/base_info_edit.html")
    c = RequestContext(
        request, {
            'form': UserInfo(instance=request.user)
        }
    )
    return HttpResponse(vt.render(c))
