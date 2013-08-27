#!/usr/bin/env python
#coding=utf-8
'''
Created on 2012-2-14

@author: Chine
'''

from django.contrib import admin

from models import SocialItem

class SocialItemAdmin(admin.ModelAdmin):
    list_display = ('share_id', 'share_id_str', 'to_share_id', 'to_share_id_str', 'type', 'share_obj','created')
    list_per_page = 10

admin.site.register(SocialItem, SocialItemAdmin)