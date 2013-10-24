#! -*- coding:utf-8 -*-
import json
from django.template import loader, RequestContext
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils.datastructures import MultiValueDictKeyError
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.conf import settings

from accounts.forms import register_form
from groups.models import Topic, Category, Group
from sys_notification.models import Notification


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
            groups_list = Group.objects.filter(category__id=request.GET["c_id"]).order_by("-last_topic_add")
        except MultiValueDictKeyError:
            groups_list = Group.objects.filter(category__name="互联网/电子商务").order_by("-last_topic_add")
        # 对群组分页
        paginator = Paginator(groups_list, settings.PAGINATION_PER_PAGE)
        page = request.GET.get('page')
        try:
            groups = paginator.page(page)
        except PageNotAnInteger:
            groups = paginator.page(1)
        except EmptyPage:
            groups = paginator.page(paginator.num_pages)


    recent_topics = Topic.objects.filter(status='enabled').order_by("-last_reply_add")[:5]
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


def search(request):
    """
    搜索群组和话题
    """
    categories = Category.objects.filter(parent__isnull=True)  # 顶级分类
    content = request.GET['search_content']
    try:
        ty = request.GET['ty']    # 类型:群组/话题
        if ty == 'group':
            group_qs_list = Group.objects.filter(name__icontains=content).distinct()
            # 对群组分页
            paginator = Paginator(group_qs_list, settings.PAGINATION_PER_PAGE)
            page = request.GET.get('page')
            print paginator.page()
            try:
                group_qs = paginator.page(page)
            except PageNotAnInteger:
                group_qs = paginator.page(1)
            except EmptyPage:
                group_qs = paginator.page(paginator.num_pages)
            ctx = {
                'groups': group_qs,
                'topics': None,
                'categories': categories,
                'content': content,
                'ty':ty
            }
        elif ty == 'topic':
            topic_qs_list = Topic.objects.filter(name__icontains=content, status='enabled').distinct()
            # 对话题分页
            paginator = Paginator(topic_qs_list, settings.PAGINATION_PER_PAGE)
            page = request.GET.get('page')
            try:
                topic_qs = paginator.page(page)
            except PageNotAnInteger:
                topic_qs = paginator.page(1)
            except EmptyPage:
                topic_qs = paginator.page(paginator.num_pages)
            ctx = {
                'groups': None,
                'topics': topic_qs,
                'categories': categories,
                'content': content,
                'ty': ty
            }
        return render(request, 'search_result.html', ctx)
    except MultiValueDictKeyError:
        ctx = {
            'groups': None,
            'topics': None,
            'ty': None,
            'content': content,
            'categories': categories
        }
        return render(request, 'search_result.html', ctx)


def get_messages(request):
    """
    ajax轮询,用于发送通知
    """
    notification = {}
    t_user_notify_qs = Notification.objects.filter(to_user=request.user, click='unclick').distinct()
    for_group = t_user_notify_qs.filter(no_type='group')
    for_topic = t_user_notify_qs.filter(no_type='topic')
    notification['for_group'] = len(for_group)
    notification['for_topic'] = len(for_topic)
    notification['all'] = len(t_user_notify_qs)
    return HttpResponse(json.dumps(notification, ensure_ascii=False), mimetype="application/json")


