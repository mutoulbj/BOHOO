# coding=utf-8
# -*- coding:utf-8 -*-
import json
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.template import loader, RequestContext
from django.shortcuts import redirect
from django.contrib.auth import logout

from User.models import MyUser
from User.forms import UserInfo


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