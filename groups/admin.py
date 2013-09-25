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



class ApplicantAdmin(admin.ModelAdmin):
    list_display = ('applicant', 'group', 'reason', 'join_type', 'status')
    list_filter = ('group', 'join_type', 'status')
    actions = ['pass_apply', 'reject_apply']

    def pass_apply(self, request, queryset):
        """ 通过申请 @fanlintao """
        can_treat = True
        for q in queryset:
            if q.status != 'processing':
                can_treat = False
                continue
        if can_treat:
            for q in queryset:
                if q.join_type == "manager":
                    q.group.manager.add(q.applicant)  # 将申请人加进小组管理员
                    q.status = "pass"
                    q.save()
                elif q.join_type == "member":
                    q.group.member.add(q.applicant)   # 将申请人加进组员
                    q.status = "pass"
                    q.save()
            msg = u"已经通过所有申请"
        else:
            msg = u"只有状态为processing的记录能操作,请确认!"
        self.message_user(request, msg)
        # TODO  修改错误时的显示方式

    pass_apply.short_description = u"通过申请"

    def reject_apply(self, request, queryset):
        """ 拒绝申请 @fanlintao """
        can_treat = True
        for q in queryset:
            if q.status != 'processing':
                can_treat = False
                continue
        if can_treat:
            queryset.update(status="reject")
            msg = u"已经驳回所有申请"
        else:
            msg = u"只有状态为processing的记录能操作,请确认!"
        self.message_user(request, msg)
    reject_apply.short_description = u"拒绝申请"

admin.site.register(Applicant, ApplicantAdmin)