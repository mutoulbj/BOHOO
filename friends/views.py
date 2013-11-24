#! -*- coding:utf-8 -*-
import json
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse

from friends.models import Friendship
from User.models import MyUser
from sys_notification.signals import friend_notify


@login_required()
def follow(request, user_id):
    """关注 @fanlintao 20131105"""
    error = {'success': '', 'error': ''}
    t_user = get_object_or_404(MyUser, pk=user_id)
    f = Friendship(from_user=request.user, to_user=t_user)
    f.save()
    error['success'] = 'success'
    return HttpResponse(json.dumps(error, ensure_ascii=False), mimetype="application/json")


def friend_tooltip(request):
    """关注的提示框 @fanlintao 20131106"""
    t_id = request.GET['t_id']
    user = get_object_or_404(MyUser, pk=t_id)
    is_followed = True
    try:
        Friendship.objects.get(from_user=request.user, to_user=user)
    except ObjectDoesNotExist:
        is_followed = False
    ctx = {
        'user': user,
        'is_followed': is_followed
    }
    return render(request, 'friends.html', ctx)


def ajax_follow(request):
    """关注 @fanlintao 20131106 """
    error = {'success': '', 'error': ''}
    if request.method == 'POST':
        try:
            t_user = MyUser.objects.get(pk=request.POST.get('user_id'))
            try:
                Friendship.objects.get(from_user=request.user, to_user=t_user)
                error['error'] = 'error'
                return HttpResponse(json.dumps(error, ensure_ascii=False), mimetype="application/json")
            except ObjectDoesNotExist:
                f = Friendship(from_user=request.user, to_user=t_user)
                f.save()
                friend_notify.send(sender=f, instance=f)
                error['success'] = 'success'
                return HttpResponse(json.dumps(error, ensure_ascii=False), mimetype="application/json")
        except ObjectDoesNotExist:
            error['error'] = 'error'
            return HttpResponse(json.dumps(error, ensure_ascii=False), mimetype="application/json")


def ajax_unfollow(request):
    """取消关注 @fanlintao 20131106"""
    error = {'success': '', 'error': ''}
    if request.method == 'POST':
        try:
            t_user = MyUser.objects.get(pk=request.POST.get('user_id'))
            try:
                f = Friendship.objects.get(from_user=request.user, to_user=t_user)
                f.delete()
                error['success'] = 'success'
                return HttpResponse(json.dumps(error, ensure_ascii=False), mimetype="application/json")
            except ObjectDoesNotExist:
                error['error'] = 'error'
                return HttpResponse(json.dumps(error, ensure_ascii=False), mimetype="application/json")
        except ObjectDoesNotExist:
            error['error'] = 'error'
            return HttpResponse(json.dumps(error, ensure_ascii=False), mimetype="application/json")