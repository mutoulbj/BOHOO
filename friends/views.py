#! -*- coding:utf-8 -*-
import json
from django.shortcuts import get_object_or_404
from django.http import HttpResponse

from friends.models import Friendship
from User.models import MyUser


def follow(request, user_id):
    """关注 @fanlintao 20131105"""
    error = {'success': '', 'error': ''}
    t_user = get_object_or_404(MyUser, pk=user_id)
    f = Friendship(from_user=request.user, to_user=t_user)
    f.save()
    error['success'] = 'success'
    return HttpResponse(json.dumps(error, ensure_ascii=False), mimetype="application/json")

