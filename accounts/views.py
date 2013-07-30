#! -*- coding:utf-8 -*-
import json
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.template import loader, RequestContext

from accounts.forms import login_form, register_form

from User.models import MyUser


def login(request):
    """
    登录
    """
    vt = loader.get_template('login.html')
    c = RequestContext(
        request, {
            'form': login_form(),
        }
    )
    return HttpResponse(vt.render(c))


def register(request):
    """
    注册
    """
    # print request.POST
    if request.method == 'POST':
        form = register_form(request.POST)
        print form.errors
        if form.is_valid():
            # print form.cleaned_data
            form.save()
    vt = loader.get_template('register.html')
    c = RequestContext(
        request, {
            'form': register_form()
        }
    )
    return HttpResponse(vt.render(c))


def view_member_info(request):
    """
    查看他人信息
    """
    vt = loader.get_template('member_info.html')
    c = RequestContext(
        request, {

        }
    )
    return HttpResponse(vt.render(c))


def username_check(request):
    """
    用户名验证
    """
    res = {}
    if request.method == 'POST':
        username = request.POST['username']
        try:
            user = MyUser.objects.get(username=username)
            res['error'] = 'error'
            return HttpResponse(json.dumps(res))
        except ObjectDoesNotExist:
            if not username:
                res['error'] = 'error'
                return HttpResponse(json.dumps(res))
            res['error'] = 'success'
            return HttpResponse(json.dumps(res))


def email_check(request):
    """
    邮箱验证:是否已经被注册
    """
    res = {}
    if request.method == 'POST':
        email = request.POST['email']
        print email
        try:
            user = MyUser.objects.get(email=email)
            res['error'] = 'error'
            print res
            return HttpResponse(json.dumps(res))
        except ObjectDoesNotExist:
            if not email:
                res['error'] = 'error'
                return HttpResponse(json.dumps(res))
            res['error'] = 'success'
            return HttpResponse(json.dumps(res))