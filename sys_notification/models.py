#! -*- coding:utf-8 -*-
from django.db import models

from User.models import MyUser
from groups.models import Group, Topic, Reply, Applicant

# 通知类型:群组,话题,好友
NOTIFICATION_CHOICES = (('group', 'Group'), ('topic', 'Topic'), ('friend', 'Friend'))
# 群组操作: 同意,拒绝, 同意
GROUP_ACTION_CHOICES = (('pass', 'Pass'), ('reject', 'Reject'))
# 回复操作:对话题的回复,对回复的回复,删除话题,删除回复
TOPIC_ACTION_CHOICES = (('re_topic', 'Reply Topic'), ('re_reply', 'Reply Reply'), ('delete_topic', 'Delete Topic'),
                        ('delete_reply', 'Delete Reply'))
# 好友操作: 关注
FRIEND_ACTION_CHOICES = (('follow', 'Follow'),)
# 状态:未读, 已经读, 未点击,已点击
STATUS_CHOICES = (('unread', 'Unread'), ('read', 'Read'))
# 是否点击过: 未点击, 已点击
CLICK_CHOICES = (('unclick', 'Unclick'), ('clicked', 'Clicked'))


class Notification(models.Model):
    """
    通知
    no_type   通知类型
    group_action 群组操作
    topic_action 话题操作
    friend_action 好友操作
    to_user    通知的用户
    topic      话题
    group      群组
    reply      回复
    applicant  相对应的申请
    follower   关注的用户
    status     状态
    click      点击
    add_time   添加时间
    """
    no_type = models.CharField(max_length=128, verbose_name=u'通知类型', choices=NOTIFICATION_CHOICES, db_index=True)
    group_action = models.CharField(max_length=128, verbose_name=u'群组操作', choices=GROUP_ACTION_CHOICES, blank=True, null=True)
    topic_action = models.CharField(max_length=128, verbose_name=u'回复操作', choices=TOPIC_ACTION_CHOICES, blank=True, null=True)
    friend_action = models.CharField(max_length=128, verbose_name=u'好友操作', choices=FRIEND_ACTION_CHOICES, blank=True, null=True)
    to_user = models.ForeignKey(MyUser, related_name='notify_user')
    topic = models.ForeignKey(Topic, related_name='notify_topic', blank=True, null=True)
    group = models.ForeignKey(Group, related_name='notify_group', blank=True, null=True)
    reply = models.ForeignKey(Reply, related_name='notify_reply', blank=True, null=True)
    applicant = models.ForeignKey(Applicant, related_name='notify_applicant', blank=True, null=True)
    follower = models.ForeignKey(MyUser, related_name='notify_follower', blank=True, null=True)
    status = models.CharField(max_length=128, default='unread', verbose_name=u'状态', choices=STATUS_CHOICES, db_index=True)
    click = models.CharField(max_length=128, default='unclick', choices=CLICK_CHOICES, db_index=True)
    add_time = models.DateTimeField(auto_now_add=True, verbose_name=u'添加时间')

    def __unicode__(self):
        return u"通知,类型: %s" % self.no_type

    class Meta:
        verbose_name = u'通知'
        verbose_name_plural = u'通知'
        db_table = 'notification'