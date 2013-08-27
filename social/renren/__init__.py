#!/usr/bin/env python
#coding=utf-8

import urllib2, json, urllib, time, hashlib

from django.conf import settings

def get_auth_json(code):
    auth_url = settings.RENREN_ACCESS_TOKEN_ENDPOINT
    body = urllib.urlencode({
                'code': code,
                'client_id': settings.RENREN_API['api_key'],
                'client_secret': settings.RENREN_API['secret_key'],
                'redirect_uri': settings.RENREN_API['redirect_urls'],
                'grant_type': 'authorization_code',
                })
    req = urllib2.Request(auth_url, body)
    resp = urllib2.urlopen(req)
    
    data = json.loads(resp.read())
    data['expires'] = data['expires_in'] + time.time()
    
    return data

def get_signature(params, secret):
    params_str = ''.join(['%s=%s'%(k, params[k]) for k in sorted(params)])
    
    return hashlib.md5("%s%s"%(params_str, secret)).hexdigest()

def get_blog_user(auth_data):
    access_token = auth_data['access_token']
    if time.time() < auth_data['expires']:
        params = {
                  'method': 'users.getInfo', 
                  'v': '1.0',
                  'access_token': access_token,
                  'format': 'JSON',
                  'fields': 'name,tinyurl'
                  }
        
        sig = get_signature(params, settings.RENREN_API['secret_key'])
        params['sig'] = sig
        params = urllib.urlencode(params)
        
        req = urllib2.Request(settings.RENREN_API_ENDPOINT, params)
        resp = urllib2.urlopen(req)
        
        data = json.loads(resp.read())[0]
        
        blog_user = {
                     'username' : data['name'],
                     'avatar': data['tinyurl']
                     }
        
        return blog_user
    
class BlogRenrenClient(object):
    def __init__(self, auth_data):
        if isinstance(auth_data, dict):
            self.access_token = auth_data['access_token']
            self.expires = auth_data['expires']
            self.refresh_token = auth_data['refresh_token']
        elif isinstance(auth_data, str):
            self.access_token, self.expires = None, None
            self.refresh_token = auth_data
        else:
            self.access_token = getattr(auth_data, 'access_token')
            self.expires = getattr(auth_data, 'expires')
            self.refresh_token = getattr(auth_data, 'refresh_token')
            
    def _call(self, method, **kwargs):
        params = {
              'method': method, 
              'v': '1.0',
              'access_token': self.access_token,
              'format': 'JSON',
              }
        params.update(kwargs)
        
        sig = get_signature(params, settings.RENREN_API['secret_key'])
        params['sig'] = sig
        params = urllib.urlencode(params)
        
        req = urllib2.Request(settings.RENREN_API_ENDPOINT, params)
        resp = urllib2.urlopen(req)
        
        data = json.loads(resp.read())
        
        return data
    
    def _refresh_token(self):
        auth_url = settings.RENREN_ACCESS_TOKEN_ENDPOINT
        body = urllib.urlencode({
                    'refresh_token': self.refresh_token,
                    'client_id': settings.RENREN_API['api_key'],
                    'client_secret': settings.RENREN_API['secret_key'],
                    'grant_type': 'refresh_token',
                    })
        req = urllib2.Request(auth_url, body)
        resp = urllib2.urlopen(req)
        
        data = json.loads(resp.read())
        self.expires = data['expires_in'] + time.time()
        self.access_token = data['access_token'].encode('utf-8')
        
    def update_status(self, content):
        content = content.encode('utf-8')
        result = self.__call__("status.set", status=content)
        
        # print result
        return 'result' in result and result['result'] == 1
            
    def __call__(self, method, **kwargs):
        if self.expires and self.access_token and self.expires > time.time():
            try:
                return self._call(method, **kwargs)
            except urllib2.HTTPError:
                self._refresh_token()
                return self._call(method, **kwargs)
        else:
            self._refresh_token()
            return self._call(method, **kwargs)
            
client = BlogRenrenClient(settings.RENREN_API['refresh_token'])