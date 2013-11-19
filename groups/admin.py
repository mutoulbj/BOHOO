#coding=utf-8

from django.contrib import admin
from models import Category, Group, Topic, Report, Applicant, Reply
from django.contrib import messages

from sys_notification.signals import group_notify


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'parent')

admin.site.register(Category, CategoryAdmin)


class GroupAdmin(admin.ModelAdmin):
    date_hierarchy = 'create_time'
    list_display = ('name', 'creator', 'group_type', 'create_time', 'modify_time', 'is_closed', 'last_topic_add')
    list_filter = ('creator', 'group_type', 'is_closed', 'place')

admin.site.register(Group, GroupAdmin)


class TopicAdmin(admin.ModelAdmin):
    date_hierarchy = 'create_time'
    list_display = ('name', 'group', 'creator', 'create_time', 'modify_time', 'is_closed', 'last_reply_add')
    list_filter = ('creator', 'is_closed', 'status')
    #search_fields = ('id',)

admin.site.register(Topic, TopicAdmin)


class ReplyAdmin(admin.ModelAdmin):
    date_hierarchy = 'create_time'
    list_display = ('content', 'creator', 'topic', 'create_time', 'reply', 'status')
    list_filter = ('status', 'creator',)
    #search_fields = ('id',)

admin.site.register(Reply, ReplyAdmin)


class ReportAdmin(admin.ModelAdmin):
    list_display = ('report_type', 'reason', 'is_handle')
    list_filter = ('report_type', 'is_handle')
    actions = ['keep', 'del_report_content']

    # 保持原状
    def keep(self, request, queryset):
        """ 保持原状 @fanlintao """
        for r in queryset:
            r.is_handle = True
            r.save()
        msg = u"保持原状操作成功"
        self.message_user(request, msg)
    keep.short_description = u"保持原状"

    # 禁用举报的内容
    def del_report_content(self, request, queryset):
        """禁用举报的内容 @fanlintao """
        can_treat = True
        for r in queryset:
            if r.is_handle:
                can_treat = False
                continue
        if can_treat:
            for r in queryset:
                if r.report_type == 'topic':
                    r.topic.status = 'disabled'
                    r.topic.save()
                    r.is_handle = True
                    r.save()
                elif r.report_type == 'reply':
                    r.reply.status = 'disabled'
                    r.reply.save()
                    r.is_handle = True
                    r.save()
            msg = u"已经禁用所有举报的内容"
            self.message_user(request, msg)
        else:
            msg = u"只有未处理过的记录能操作,请确认!"
            messages.add_message(request, messages.ERROR, msg)
    del_report_content.short_description = u"禁用举报内容"


admin.site.register(Report, ReportAdmin)


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
                group_notify.send(sender=q, instance=q)   # 发送signal
            msg = u"已经通过所有申请"
            self.message_user(request, msg)
        else:
            msg = u"只有状态为processing的记录能操作,请确认!"
            messages.add_message(request, messages.ERROR, msg)
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
            for q in queryset:
                group_notify.send(sender=q, instance=q)   # 发送signal
            msg = u"已经驳回所有申请"
            self.message_user(request, msg)
        else:
            msg = u"只有状态为processing的记录能操作,请确认!"
            messages.add_message(request, messages.ERROR, msg)

    reject_apply.short_description = u"拒绝申请"

admin.site.register(Applicant, ApplicantAdmin)





