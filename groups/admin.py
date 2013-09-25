#coding=utf-8

from django.contrib import admin
from models import Category, Group, Topic, Report, Applicant


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'parent')

admin.site.register(Category, CategoryAdmin)


class GroupAdmin(admin.ModelAdmin):
    date_hierarchy = 'create_time'
    list_display = ('name', 'creator', 'group_type', 'create_time', 'modify_time', 'is_closed', 'last_topic_add')
    list_filter = ('creator', 'group_type', 'is_closed')

admin.site.register(Group, GroupAdmin)


class TopicAdmin(admin.ModelAdmin):
    date_hierarchy = 'create_time'
    list_display = ('name', 'group', 'creator', 'create_time', 'modify_time', 'is_closed', 'last_reply_add')
    list_filter = ('creator', 'is_closed')
    search_fields = ('id',)

admin.site.register(Topic, TopicAdmin)


class ReportAdmin(admin.ModelAdmin):
    list_display = ('report_type', 'reason', 'is_handle')
    list_filter = ('report_type', 'is_handle')


admin.site.register(Report, ReportAdmin)


# 申请相关处理
def pass_apply(modeladmin, request, queryset):
    """ 通过申请 @fanlintao """
    queryset.update(status="pass")
pass_apply.short_description = u"通过申请"


def reject_apply(modeladmin, request, queryset):
    """ 拒绝申请 @fanlintao """
    queryset.update(status="reject")
reject_apply.short_description = u"拒绝申请"


class ApplicantAdmin(admin.ModelAdmin):
    list_display = ('applicant', 'group', 'reason', 'join_type', 'status')
    list_filter = ('group', 'join_type', 'status')
    actions = [pass_apply, reject_apply]

admin.site.register(Applicant, ApplicantAdmin)