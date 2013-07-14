#coding=utf-8

'''
@author: 潘飞(cnweike@gmail.com)
'''

from django.contrib import admin
from models import *

class CatelogAdmin(admin.ModelAdmin):
	list_display = ('cate_name','id','parent_id')
	
admin.site.register(Catelog,CatelogAdmin)

class GroupAdmin(admin.ModelAdmin):
	date_hierarchy = 'create_time'
	list_display = ('name', 'creator', 'type', 'create_time', 'modify_time', 'is_closed', 'last_topic_add')
	list_filter = ('creator', 'type', 'is_closed')
	
admin.site.register(Group, GroupAdmin)

class Group_topic_amountAdmin(admin.ModelAdmin):
	list_display = ('group', 'amount')
	
admin.site.register(Group_topic_amount, Group_topic_amountAdmin)

class TopicAdmin(admin.ModelAdmin):
	date_hierarchy = 'create_time'
	list_display = ('name', 'group', 'creator', 'create_time', 'modify_time', 'is_closed', 'last_reply_add')
	list_filter = ('creator', 'is_closed')
	search_fields = ('id',)
	
admin.site.register(Topic, TopicAdmin)

class Topic_reply_amountAdmin(admin.ModelAdmin):
	list_display = ('topic', 'amount')
	
admin.site.register(Topic_reply_amount, Topic_reply_amountAdmin)

class ReplyAdmin(admin.ModelAdmin):
	date_hierarchy = 'create_time'
	list_display = ('creator', 'topic', 'create_time')
	list_filter = ('creator',)
	search_fields = ('id',)
	
admin.site.register(Reply, ReplyAdmin)

class Group_memeberAdmin(admin.ModelAdmin):
	date_hierarchy = 'create_time'
	list_display = ('group', 'member', 'create_time')
	list_filter = ('group', 'member_role')
	
admin.site.register(Group_memeber, Group_memeberAdmin)

class ReportAdmin(admin.ModelAdmin):
	list_display = ('rep_type', 'beReported', 'reason','is_handle')
	list_filter = ('rep_type', 'is_handle')

admin.site.register(Report, ReportAdmin)