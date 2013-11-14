# coding=utf-8
# -*- coding:utf-8 -*-
import json
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.template import loader, RequestContext
from django.shortcuts import redirect, get_object_or_404

from User.models import MyUser
from User.forms import UserInfo
from friends.models import Friendship


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
    user = MyUser.objects.get(id=tid)
    vt = loader.get_template("people/profile.html")
    c = RequestContext(
        request, {
            'user': user
        }
    )
    return HttpResponse(vt.render(c))


def view_info(request, tid):
    """
    查看他人资料
    @fanlintao
    """
    t_user = get_object_or_404(MyUser, id=tid)
    is_followed = False
    f_list = Friendship.objects.filter(from_user=request.user, to_user=t_user).values_list('from_user', flat=True)
    if request.user.id in f_list:
        is_followed = True
    vt = loader.get_template("people/info.html")
    c = RequestContext(
        request, {
            't_user': t_user,
            'is_followed': is_followed
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
