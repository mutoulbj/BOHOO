#! -*- coding:utf-8 -*-
from django.template import loader, RequestContext
from django.http import HttpResponse
from django.shortcuts import redirect

from accounts.forms import register_form


def index(request):
    """
    首页index
    若未登录显示
    """
    if request.method == "POST":
        form = register_form(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')   # 跳转到登录页面
    vt = loader.get_template("index.html")
    c = RequestContext(
        request, {
            'form': register_form(large_input=False)
        }

    )
    return HttpResponse(vt.render(c))

