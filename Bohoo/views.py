#! -*- coding:utf-8 -*-
from django.template import loader, RequestContext
from django.http import HttpResponse
from django.shortcuts import redirect

from accounts.forms import register_form
from groups.models import Topic, Category, Group


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
    if request.method == "GET":
        try:
            groups = Group.objects.filter(category__id=request.GET["c_id"]).order_by("-create_time")[:30]
        except:
            groups = Group.objects.filter(category__name="互联网/电子商务").order_by("-create_time")[:30]
    recent_topics = Topic.objects.all().order_by("-create_time")[:5]
    categories = Category.objects.filter(parent__isnull=True)  # 顶级分类
    init_ca_id = Category.objects.get(name="互联网/电子商务").id   #初始化的分类的id
    init_ca_parent_id = Category.objects.get(name="互联网/电子商务").parent.id
    vt = loader.get_template("index.html")
    c = RequestContext(
        request, {
            'form': register_form(large_input=False),
            'recent_topics': recent_topics,
            'categories': categories,
            'groups': groups,
            'init_ca_id': init_ca_id,
            'init_ca_parent_id': init_ca_parent_id,
        }
    )
    return HttpResponse(vt.render(c))

