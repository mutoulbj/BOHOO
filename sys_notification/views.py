#! -*- coding:utf-8 -*-
import json
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render

from sys_notification.models import Notification


def notify_group(request):
    """
    通知:群组
    @fanlintao
    """
    group_notify = Notification.objects.filter(to_user=request.user, no_type='group', status='unread').order_by('-add_time')
    ctx = {
        'group_notify': group_notify,
        'active': 'group'
    }
    return render(request, 'notify/groups.html', ctx)


def notity_topic(request):
    """
    通知:话题
    @fanlintao
    """
    topic_notify = Notification.objects.filter(to_user=request.user, no_type='topic', status='unread').order_by('-add_time')
    ctx = {
        'topic_notify': topic_notify,
        'active': 'topic'
    }
    return render(request, 'notify/topic.html', ctx)


def del_notify(request):
    """
    通知:不再提醒
    """
    error = {}
    try:
        notify = Notification.objects.get(id=request.POST['n_id'])
        notify.delete()
        error['error'] = 'success'
        return HttpResponse(json.dumps(error, ensure_ascii=False), mimetype="application/json")
    except ObjectDoesNotExist:
        error['error'] = 'error'
        pass