#! -*- coding:utf-8 -*-
from django.template import loader, RequestContext
from django.http import HttpResponse

from accounts.forms import register_form


def index(request):
    """
    首页index
    若未登录显示
    """
    vt = loader.get_template("index.html")
    c = RequestContext(
        request, {
            'form': register_form(large_input=False)
        }

    )
    return HttpResponse(vt.render(c))
