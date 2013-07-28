#! -*- coding:utf-8 -*-

from django.http import HttpResponse
from django.template import loader, RequestContext

from accounts.forms import login_form, register_form


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