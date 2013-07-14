#! -*- coding:utf-8 -*-
from django.template import loader, RequestContext
from django.http import HttpResponse


def index(request):
    """
    首页index
    """
    vt = loader.get_template("index.html")
    c = RequestContext(
        request,

    )
    return HttpResponse(vt.render(c))
