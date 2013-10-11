#! -*- coding:utf-8 -*-
import json
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.template import loader, RequestContext
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.core.mail import send_mail
from django.conf import settings
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.utils.datastructures import MultiValueDictKeyError

from accounts.forms import login_form, register_form, password_reset_apply_form, reset_password_form

from User.models import MyUser


def login(request):
    """
    登录
    """
    if request.method == 'POST':
        form = login_form(request, request.POST)
        if form.is_valid():
            from django.contrib.auth import login
            login(request, form.get_user())
            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()
            return redirect("/")
    else:
        form = login_form(request)
        request.session.set_test_cookie()
    vt = loader.get_template('login.html')
    c = RequestContext(
        request, {
            'form': form,
        }
    )
    return HttpResponse(vt.render(c))


def register(request):
    """
    注册
    """
    if request.method == 'POST':
        form = register_form(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')   # 跳转到登录页面
    vt = loader.get_template('register.html')
    c = RequestContext(
        request, {
            'form': register_form()
        }
    )
    return HttpResponse(vt.render(c))


@login_required()
def log_out(request):
    """
    注销
    """
    logout(request)
    return redirect('/')


def view_member_info(request):
    """
    查看他人信息
    """
    vt = loader.get_template('member_info.html')
    c = RequestContext(
        request, {

        }
    )
    return HttpResponse(vt.render(c))


def username_check(request):
    """
    用户名验证
    """
    res = {}
    if request.method == 'POST':
        username = request.POST['username']
        try:
            user = MyUser.objects.get(username=username)
            res['error'] = 'error'
            return HttpResponse(json.dumps(res))
        except ObjectDoesNotExist:
            if len(username.encode('gbk')) > 14:   # 用户名长度大于14个字节
                res['error'] = 'error'
                return HttpResponse(json.dumps(res))
            if not username:
                res['error'] = 'error'
                return HttpResponse(json.dumps(res))
            res['error'] = 'success'
            return HttpResponse(json.dumps(res))


def email_check(request):
    """
    邮箱验证:是否已经被注册
    """
    res = {}
    if request.method == 'POST':
        email = request.POST['email']
        try:
            user = MyUser.objects.get(email=email)
            res['error'] = 'error'
            return HttpResponse(json.dumps(res))
        except ObjectDoesNotExist:
            if not email:
                res['error'] = 'error'
                return HttpResponse(json.dumps(res))
            res['error'] = 'success'
            return HttpResponse(json.dumps(res))


def reset_password_apply(request):
    """
    请求重置密码
    """
    if request.method == 'POST':
        form = password_reset_apply_form(request.POST)
        if form.is_valid():
            import time
            import hashlib
            t_email = form.get_email()
            user_id = str(MyUser.objects.get(email=t_email).id)
            timestamp = str(time.time())
            key = settings.HASH_KEY
            l_str = user_id + timestamp + key
            m = hashlib.md5()
            m.update(l_str)
            hash_code = m.hexdigest()
            url = request.build_absolute_uri(reverse('reset_password', kwargs={'user_id': 0})) + \
                  '?id=' + user_id + '&timestamp=' + timestamp + '&hash_code=' + hash_code
            subject = u'密码重置'
            message = u'请点击下面的连接进行密码重置,如果不能点击请将链接复制到浏览器地址栏中打开.%s' % url
            send_mail(subject, message, settings.EMAIL_HOST_USER, [t_email, ])
            return render(request, 'reset_password_email_sent.html', {'email': t_email})
    else:
        form = password_reset_apply_form()
    return render(request, 'reset_password_apply.html', {'form': form})


def reset_password(request, user_id=None):
    """"重置密码"""
    import time
    import hashlib
    timestamp = None
    try:
        timestamp = request.GET['timestamp']
    except MultiValueDictKeyError:
        pass

    if timestamp:
        if time.time() - float(timestamp) > 3600:    # 超过1小时连接失效
            return render(request, 'reset_password_invalid.html', {'invalid_reason': 'timeout'})
        else:
            key = settings.HASH_KEY
            user_id = request.GET['id']
            hash_code = request.GET['hash_code']
            m = hashlib.md5()
            m.update(user_id+timestamp+key)
            if hash_code != m.hexdigest():   # hash值不正确,连接无效
                return render(request, 'reset_password_invalid.html', {'invalid_reason': 'invalid_link'})
    try:
        user = MyUser.objects.get(id=user_id)
        if request.method == 'POST':
            form = reset_password_form(request.POST)
            if form.is_valid():
                password = form.cleaned_data['password']
                user.set_password(password)
                user.save()
                logout(request)
                return redirect(reverse('login'))
        else:
            form = reset_password_form()
        return render(request, 'reset_password.html', {'form': form})
    except ObjectDoesNotExist:
        pass

