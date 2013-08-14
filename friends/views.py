#! -*- coding:utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext_lazy as _
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from django.views.generic.edit import BaseUpdateView
from django.http.response import HttpResponseForbidden, HttpResponse

from friends.models import FriendShip
from User.models import MyUser

class MyFollow(ListView):
    template_name = 'follow.html'
    context_object_name = 'users'
    
    def get_queryset(self):
        return FriendShip.objects.get_following(self.request.user)
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(MyFollow, self).dispatch(*args, **kwargs)
myfollow = MyFollow.as_view()

class MyFans(ListView):
    template_name = 'follow.html'
    context_object_name = 'users'
    
    def get_queryset(self):
        return FriendShip.objects.get_followed(self.request.user)
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(MyFans, self).dispatch(*args, **kwargs)
myfans = MyFans.as_view()

class UserFollow(ListView):
    template_name = 'follow.html'
    context_object_name = 'users'
    
    def get_queryset(self):
        user = MyUser.objects.get(pk = self.kwargs.get('user_id', None))
        return FriendShip.objects.get_following(user)
userfollow = UserFollow.as_view()

class UserFans(ListView):
    template_name = 'follow.html'
    context_object_name = 'users'
    
    def get_queryset(self):
        user = MyUser.objects.get(pk = self.kwargs.get('user_id', None))
        return FriendShip.objects.get_followed(user)
userfans = UserFans.as_view()

class Action(BaseUpdateView):
    
    def get(self, request, *args, **kwargs):
        return HttpResponseForbidden()
    
    def post(self, request, *args, **kwargs):
        to_user = request.body.get('to_user')
        from_user = request.user
        relation = FriendShip.objects.filter(from_user = from_user, to_user = to_user).exists()
        if relation:
            FriendShip.objects.get(from_user = from_user, to_user = to_user).delete()
            return HttpResponse(_('follow'))
        else:
            FriendShip.objects.create(from_user = from_user, to_user = to_user)
            return HttpResponse(_('following'))
        
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(Followed, self).dispatch(*args, **kwargs)    
action = Action.as_view()