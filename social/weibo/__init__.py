#!/usr/bin/env python
#coding=utf-8

import urllib2, json, urllib, time

from django.conf import settings

from weibo2 import APIClient
from social.utils import count_words

def get_auth_json(code):
    auth_url = settings.WEIBO_ACCESS_TOKEN_ENDPOINT
    body = urllib.urlencode({
                'code': code,
                'client_id': settings.WEIBO_API['app_key'],
                'client_secret': settings.WEIBO_API['app_secret'],
                'redirect_uri': settings.WEIBO_API['redirect_urls'],
                'grant_type': 'authorization_code',
                })
    req = urllib2.Request(auth_url, body)
    resp = urllib2.urlopen(req)
    
    data = json.loads(resp.read())
    data['expires'] = data['expires_in'] + time.time()
    
    return data

def get_blog_user(auth_data):
    access_token = auth_data['access_token']
    if time.time() < auth_data['expires']:
        api_url = settings.WEIBO_API_ENDPOINT
        params = urllib.urlencode({
                                   'access_token': access_token,
                                   'uid': auth_data['uid']
                                   })
        
        req = urllib2.Request('%susers/show.json?%s' % (api_url, params))
        resp = urllib2.urlopen(req)
        
        data = json.loads(resp.read())
        
        blog_user = {
                     'username' : data['screen_name'],
                     'avatar': data['avatar_large'],
                     'site': data['url'],
                     'uid': data['id']
                     }
        
        return blog_user
    
class BlogWeiboClient(object):
    def __init__(self, 
                 app_key=settings.WEIBO_API['app_key'],
                 app_secret=settings.WEIBO_API['app_secret'],
                 redirect_uri=settings.WEIBO_REDIRECT_URI):
        self.client = APIClient(app_key, app_secret, redirect_uri=redirect_uri)
        
    def set_access_token(self, access_token, expires_in):
        self.client.set_access_token(access_token, expires_in)
        
    def count_words(self, content):
        return count_words(content)

    def update_status(self, content):
        r = self.client.post.statuses__update(status=content)
        return r.id
    
    def get_short_url(self, url):
        r = self.client.short_url__shorten(url_long=url)
        return r['urls'][0].url_short
    
    
client = BlogWeiboClient()