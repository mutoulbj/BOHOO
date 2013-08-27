#!/usr/bin/env python
#coding=utf-8

from django.db import models
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType

from managers import ArticleSocialItemManager, CommentSocialItemManager

class SocialItem(models.Model):
    SOURCE_CHOICE = (
        (1, '新浪微博'),
        (2, '腾讯微博'),
        (3, '人人网'),
        (4, 'Google+')
    )
    
    share_id = models.BigIntegerField(editable=False, verbose_name="分享社交网络id")
    share_id_str = models.CharField(max_length=30, editable=False, blank=True, null=True, verbose_name="分享社交网络id（非整形）")
    to_share_id = models.BigIntegerField(editable=False,blank=True, null=True, verbose_name="评论的分享社交网络id")
    to_share_id_str = models.CharField(max_length=30, editable=False, blank=True, null=True, verbose_name="评论的分享社交网络id（非整形）")
    type = models.IntegerField(choices=SOURCE_CHOICE, editable=False, verbose_name="分享社交网络类别")
    created = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    # contenttypes
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    share_obj = generic.GenericForeignKey('content_type', 'object_id')
    
    objects = models.Manager()
    to_article_objects = ArticleSocialItemManager()
    to_comment_objects = CommentSocialItemManager()
    
    class Meta:
        verbose_name = '社交网络'
        verbose_name_plural = '社交网络'