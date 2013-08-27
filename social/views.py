#!/usr/bin/env python
#coding=utf-8

import urllib

from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings

import google, weibo, renren, txweibo

auth_types = {
             'google': 0,
             'weibo': 1,
             'qqweibo': 2,
             'renren': 3,
             }

def _get_referer_url(request):
    referer_url = request.META.get('HTTP_REFERER', '/')
    host = request.META['HTTP_HOST']
    if referer_url.startswith('http') and host not in referer_url:
        referer_url = '/'
    return referer_url

def logout(request):
    if 'blog_user' in request.session:
        del request.session['blog_user']
        
    return HttpResponseRedirect(_get_referer_url(request))

def google_login(request):
    kwargs = {
       'response_type': 'code',
       'client_id': settings.GOOGLE_API['client_id'],
       'redirect_uri': settings.GOOGLE_REDIRECT_URI,
       'scope': 'https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile',
       'state': _get_referer_url(request)
    }
    
    if 'from' in request.GET and request.GET['from'] == 'admin':
        kwargs['scope'] = '%s %s' % (kwargs['scope'], 'https://www.googleapis.com/auth/plus.me')
        kwargs['access_type'] = 'offline'
    
    google_auth_url = '%s?%s' % (settings.GOOGLE_AUTH_ENDPOINT,
                             urllib.urlencode(kwargs))
    return HttpResponseRedirect(google_auth_url)

def google_auth(request):
    if 'blog_user' in request.session:
        return HttpResponseRedirect('/')
    
    if 'error' in request.GET or 'code' not in request.GET:
        return HttpResponseRedirect('/')
    
    code = request.GET['code']
    
    access_token = google.get_access_token(code)
    blog_user = google.get_blog_user(google.get_user_info(access_token))
    
    blog_user['auth_type'] = auth_types['google']
    blog_user['access_token'] = access_token
    request.session['blog_user'] = blog_user
    
#    resp = HttpResponse()
#    resp.write(request.session['blog_user'].username)
#    resp.write(request.session['blog_user'].access_token)
#    return resp
    
    next = '/'
    if 'state' in request.GET:
        next = request.GET['state']
    
    return HttpResponseRedirect(next)

def weibo_login(request):
    weibo_auth_url = '%s?%s' % (settings.WEIBO_AUTH_ENDPOINT,
                             urllib.urlencode({
                                               'response_type': 'code',
                                               'client_id': settings.WEIBO_API['app_key'],
                                               'redirect_uri': settings.WEIBO_REDIRECT_URI,
                                               }))    
    request.session['redirect_uri'] = _get_referer_url(request)
    
    return HttpResponseRedirect(weibo_auth_url)
    
def weibo_auth(request):
    if 'error' in request.GET or 'code' not in request.GET:
        return HttpResponseRedirect('/')
    
    code = request.GET['code']
    
    data = weibo.get_auth_json(code)
    
    blog_user = weibo.get_blog_user(data)
    
    blog_user['auth_type'] = auth_types['weibo']
    blog_user['access_token'] = data['access_token']
    blog_user['expires'] = data['expires']
    request.session['blog_user'] = blog_user
    
    next = request.session['redirect_uri']
    del request.session['redirect_uri']
    
    return HttpResponseRedirect(next)

def renren_login(request):
    kwargs = {
       'response_type': 'code',
       'client_id': settings.RENREN_API['api_key'],
       'redirect_uri': settings.RENREN_REDIRECT_URI,
    }
    if 'from' in request.GET and request.GET['from'] == 'admin':
        kwargs['scope'] = 'publish_share status_update'
    
    renren_auth_url = '%s?%s' % (settings.RENREN_AUTH_ENDPOINT,
                             urllib.urlencode(kwargs))    
    request.session['redirect_uri'] = _get_referer_url(request)
    
    return HttpResponseRedirect(renren_auth_url)

def renren_auth(request):
    if 'error' in request.GET or 'code' not in request.GET:
        return HttpResponseRedirect('/')
    
    code = request.GET['code']
    
    data = renren.get_auth_json(code)
    
    blog_user = renren.get_blog_user(data)
    
    blog_user['auth_type'] = auth_types['renren']
    blog_user['access_token'] = data['access_token']
    blog_user['expires'] = data['expires']
    blog_user['refresh_token'] = data['refresh_token']
    request.session['blog_user'] = blog_user
    
#    resp = HttpResponse()
#    resp.write(blog_user['refresh_token'])
#    return resp
    
    next = request.session['redirect_uri']
    del request.session['redirect_uri']
    
    return HttpResponseRedirect(next)

def qqweibo_login(request):
    oauth_handler = txweibo.get_oauth_handler()
    qqweibo_auth_url = oauth_handler.get_authorization_url()
    request.session['redirect_uri'] = _get_referer_url(request)
    request.session['request_token'] = (oauth_handler.request_token.key, oauth_handler.request_token.secret)
    
    return HttpResponseRedirect(qqweibo_auth_url)

def qqweibo_auth(request):
    if 'oauth_verifier' not in request.GET:
        return HttpResponseRedirect('/')
    
    verifier = request.GET['oauth_verifier']
    request_token = request.session['request_token']
    del request.session['request_token']
    
    oauth_handler = txweibo.get_oauth_handler()
    oauth_handler.set_request_token(request_token[0], request_token[1])
    access_token = oauth_handler.get_access_token(verifier)
    
    blog_user = txweibo.get_blog_user(access_token)
    
    blog_user['auth_type'] = auth_types['qqweibo']
    blog_user['access_token'] = (access_token.key, access_token.secret)
    request.session['blog_user'] = blog_user
    
    next = request.session['redirect_uri']
    del request.session['redirect_uri']
    
    return HttpResponseRedirect(next)