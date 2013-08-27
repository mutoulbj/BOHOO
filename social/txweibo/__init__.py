#!/usr/bin/env python
#coding=utf-8

from django.conf import settings

from qqweibo import OAuthHandler, API
from social.weibo import client as weibo_client
from social.google import get_short_url

def get_oauth_handler():
    return OAuthHandler(settings.QQWEIBO_API['app_key'], 
                        settings.QQWEIBO_API['app_secret'],
                        callback=settings.QQWEIBO_API['redirect_urls'])
    
def get_blog_user(access_token):
    oauth_handler = get_oauth_handler()
    oauth_handler.setToken(access_token.key, access_token.secret)
    api = API(oauth_handler)
    
    user = api.user.info()
    
    blog_user = {
                 'username' : user.nick,
                 'avatar': user.head,
                 'email': user.email
                 }
    
    return blog_user

class BlogQQWeiboClient(object):
    def __init__(self, 
                 app_key=settings.QQWEIBO_API['app_key'],
                 app_secret=settings.QQWEIBO_API['app_secret'],
                 access_token_key=settings.QQWEIBO_API['access_token_key'], 
                 access_token_secret=settings.QQWEIBO_API['access_token_secret']):
        self.oauth_handler = get_oauth_handler()
        self.oauth_handler.setToken(access_token_key, access_token_secret)
        self.client = API(self.oauth_handler)
        
    def count_words(self, content):
        return weibo_client.count_words(content)

    def update_status(self, content):
        r = self.client.t.add(content=content)
        return r.id
    
    def get_short_url(self, url):
        # return weibo_client.get_short_url(url)
        return get_short_url(url)
    
client = BlogQQWeiboClient()