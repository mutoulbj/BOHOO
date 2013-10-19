#! -*- coding:utf-8 -*-
from django.db.models.signals import post_save
from groups.models import Group, Topic, Reply, Applicant
from sys_notification.models import Notification


def group_action(sender, instance, **kwargs):
    print 11111111111
    obj = instance
    if obj.status != 'processing':
        print 22222
        notify = Notification(no_type='group', group_action=obj.status, to_user=obj.applicant, group=obj.group)
        notify.save()
        print 333333

post_save.connect(group_action, sender=Applicant, dispatch_uid='create_group_notify')


