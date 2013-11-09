#! -*- coding:utf-8 -*-
import json
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render
from sys_notification.signals import set_notity_clicked
from sys_notification.models import Notification


@login_required()
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
    set_notity_clicked.send(sender=group_notify, request=request, no_type='group')
    return render(request, 'notify/groups.html', ctx)


@login_required()
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
    set_notity_clicked.send(sender=topic_notify, request=request, no_type='topic')
    return render(request, 'notify/topic.html', ctx)


@login_required()
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