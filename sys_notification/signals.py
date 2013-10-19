#! -*- coding:utf-8 -*-
from django.dispatch import Signal
from django.db.models.signals import post_save
from groups.models import Group, Topic, Reply, Applicant
from sys_notification.models import Notification

# 群组操作的signal
group_notify = Signal(providing_args=["instance", "args", "kwargs"])

# 话题操作的signal
topic_notify = Signal(providing_args=["instance", "args", "kwargs"])

# 好友操作的signal
# TODO: todo


def group_action(sender, instance, *args, **kwargs):
    obj = instance
    if obj.status != 'processing':
        notify = Notification(no_type='group', group_action=obj.status, to_user=obj.applicant, group=obj.group)
        notify.save()

group_notify.connect(group_action, dispatch_uid='create_group_notify')


def topic_action(sender, instance, *args, **kwargs):
    obj = instance
    if obj.reply:   # 是否是对回复的回复
        notify = Notification(no_type='topic', topic_action='re_reply', to_user=obj.reply.creator, reply=obj.reply,
                              topic=obj.topic, )
        notify.save()
    else:
        notify = Notification(no_type='topic', topic_action='re_topic', to_user=obj.topic.creator, topic=obj.topic)
        notify.save()

topic_notify.connect(topic_action, dispatch_uid='create_topic_notify')



