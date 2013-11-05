#! -*- coding:utf-8 -*-

from django.db import models

from User.models import MyUser


class Friendship(models.Model):
    """
    ``好友``
    from_user    关注
    to_user      被关注者
    add_time     添加时间
    is_blocked   拉黑
    """
    from_user = models.ForeignKey(MyUser, related_name="from_user")
    to_user = models.ForeignKey(MyUser, related_name="to_user")
    add_time = models.DateTimeField(verbose_name=u'添加时间', auto_now_add=True)
    is_blocked = models.BooleanField(verbose_name=u'拉黑', default=False)

    def __unicode__(self):
        return "Friendship from %s to %s " % (self.from_user, self.to_user)

    class Meta:
        verbose_name = u'好友'
        verbose_name_plural = u'好友'
        db_table = 'friends'
