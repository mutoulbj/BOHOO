#!/usr/bin/env python
#coding=utf-8
'''
Created on 2012-2-14

@author: Chine
'''

from django.db import models
from django.db.models import Q

class ArticleSocialItemManager(models.Manager):
    def get_query_set(self):
        return super(ArticleSocialItemManager, self)\
                    .get_query_set()\
                    .filter(Q(content_type__app_label="blog")
                            &Q(content_type__model="article"))
                    
class CommentSocialItemManager(models.Manager):
    def get_query_set(self):
        return super(CommentSocialItemManager, self)\
                    .get_query_set()\
                    .filter(Q(content_type__app_label="blog")
                            &Q(content_type__model="comment"))