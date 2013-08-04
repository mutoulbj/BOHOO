# coding=utf-8
# -*- coding:utf-8 -*-
import json
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.template import loader, RequestContext
from django.shortcuts import redirect
from django.contrib.auth import logout

from User.models import MyUser


def edit(request):
    """
    编辑个人资料
    """
    vt = loader.get_template("people/edit.html")
    c = RequestContext(
        request,
    )
    return HttpResponse(vt.render(c))