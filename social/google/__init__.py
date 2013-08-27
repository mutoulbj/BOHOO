#!/usr/bin/env python
#coding=utf-8

import urllib2, json, urllib, time

from django.conf import settings

def get_access_token(code):
    auth_url = settings.GOOGLE_ACCESS_TOKEN_ENDPOINT
    body = urllib.urlencode({
                'code': code,
                'client_id': settings.GOOGLE_API['client_id'],
                'client_secret': settings.GOOGLE_API['client_secret'],
                'redirect_uri': settings.GOOGLE_API['redirect_urls'],
                'grant_type': 'authorization_code'
                })
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    req = urllib2.Request(auth_url, body, headers)
    resp = urllib2.urlopen(req)
    
    data = json.loads(resp.read())
    
    return data['access_token']

def get_user_info(access_token):
    if access_token:
        userinfo_url = settings.GOOGLE_USERINFO_ENDPOINT
        query_string = urllib.urlencode({'access_token': access_token})
        
        resp = urllib2.urlopen("%s?%s" % (userinfo_url, query_string))
        data = json.loads(resp.read())
        
        return data
    
def get_blog_user(user_data):
    if user_data:
        blog_user = {}
        
        blog_user['username'] = user_data['name']
        blog_user['email'] = user_data['email']
        blog_user['avatar'] = user_data['picture']
        
        return blog_user
    
def get_short_url(url):
    data = json.dumps({
        'longUrl': url, 
    })
    headers = {"Content-Type": "application/json"}
    req = urllib2.Request(settings.GOOGLE_URL_SHORTENER_ENDPOINT, data, headers)
    resp = urllib2.urlopen(req)
    
    return json.loads(resp.read()).get('id', None)
    
class GooglePlusClient(object):
    def __init__(self, **kwargs):
        if 'access_token' in kwargs:
            self.access_token = kwargs['access_token']
        if 'refresh_token' in kwargs:
            self.refresh_token = kwargs['refresh_token']
            
        if 'expires' in kwargs:
            self.expires = kwargs['expires']
        elif 'expires_in' in kwargs:
            self.expires = time.time() + kwargs['expires_in']
            
    def _refresh_token(self):
        auth_url = settings.GOOGLE_ACCESS_TOKEN_ENDPOINT
        body = urllib.urlencode({
                    'client_id': settings.GOOGLE_API['client_id'],
                    'client_secret': settings.GOOGLE_API['client_secret'],
                    'refresh_token': self.refresh_token,
                    'grant_type': 'refresh_token'
                    })
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        req = urllib2.Request(auth_url, body, headers)
        resp = urllib2.urlopen(req)
        
        data = json.loads(resp.read())
        self.access_token = data['access_token']
        self.expires = time.time() + data['expires_in']
    
    def _get_access_token(self):
        if not hasattr(self, 'access_token'):
            self._refresh_token()
        return self.access_token