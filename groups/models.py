#coding=utf-8

from django.conf import settings

from django.db import models

import datetime

GROUP_TYPE_CHOICES = (('open', 'Open'), ('private', 'Private'))
MEMBER_ROLE_CHOICES = ((0, 'Member'), (1, 'Manager'), (2, 'Owner'))
MEMBER_JOIN_CHOICES = (('everyone_can_join', 'Everyone can join'), ('need_check', 'Need check'))
REPORT_TYPE_CHOICES = (('topic', u'话题'), ('reply', u'回复'))
#REASON_CHOICES = ((0, u'广告或垃圾信息'), (1, u'色情、淫秽或低俗内容'), (2, u'激进时政或意识形态话题'), (3, u'其他原因'))
STATUS_CHOICES = (('enabled', u'启用'), ('disabled', u'禁用'))


class Category(models.Model):
    """
    小组分类
    字段:
    name    分类名称
    parent  父分类
    """
    name = models.CharField(max_length=200, verbose_name=u'分类', unique=True, db_index=True)
    parent = models.ForeignKey('self', related_name="category_parent", verbose_name=u'父分类', blank=True, null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u'分类'
        verbose_name_plural = u'分类'
        db_table = 'group_category'


class Group(models.Model):
    """
    小组
    字段:
    name            名称
    description     描述
    category        分类
    creator         创建人
    member          成员
    gfriend         友情小组
    group_type      小组类型
    member_join     加入小组的方式
    create_time     创建时间
    modify_time     修改时间
    is_closed       是否关闭
    last_topic_add  上一话题创建的时间
    topic_amount    话题总数
    place   群组地点
    flag    区别某些特别群组的标志,初始化时会被赋值
    manager         管理者
    """
    name = models.CharField(max_length=255, verbose_name=u'名称', unique=True, db_index=True)
    description = models.TextField(blank=True, null=True, verbose_name=u'描述')
    category = models.ForeignKey(Category, related_name='category_group', verbose_name=u'小组分类')
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='creator_group', verbose_name=u'创建人')
    member = models.ManyToManyField(settings.AUTH_USER_MODEL)
    gfriend = models.ManyToManyField('self', symmetrical=False, verbose_name=u'友情小组')
    group_type = models.CharField(default='open', max_length=256, choices=GROUP_TYPE_CHOICES, verbose_name=u'类型')
    member_join = models.CharField(default='everyone_can_join', max_length=256, choices=MEMBER_JOIN_CHOICES,
                                   verbose_name=u'加入方式')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')
    modify_time = models.DateTimeField(default=datetime.datetime.now, verbose_name=u'修改时间')
    is_closed = models.BooleanField(default=False, verbose_name=u'是否关闭')
    last_topic_add = models.DateTimeField(null=True, blank=True, verbose_name=u'上一个话题创建的时间')
    topic_amount = models.IntegerField(default=0, verbose_name=u'话题总量')
    manager = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="user_manager", verbose_name=u"管理员")

    #add by lazytiger
    place = models.CharField(max_length=30, verbose_name=u'地点')
    flag = models.IntegerField(default=0, verbose_name=u'群组级别')
    #end add 

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u'小组'
        verbose_name_plural = u'小组'
        db_table = 'group'

    def get_group_name(self):
        return self.name

    def get_applicant_member_num(self):
        # 返回申请加入群组的人数
        return len(self.apply_group.filter(status="processing", join_type="member"))

    def get_applicant_manager_num(self):
        # 返回申请成为群组管理员的人数
        return len(self.apply_group.filter(status="processing", join_type="manager"))

    def get_members(self):
        # 返回成员数量
        return len(self.member.all())

    def get_last_reply_order_topic_qs(self, amount=5):
        """
        返回数量为amount,默认为5,以最后回复排序的话题,返回queryset
        """
        return self.group_topic.filter(status='enabled').order_by("-last_reply_add")[:amount]


class TopicImage(models.Model):
    """
    话题图片
    image 图片
    """
    image = models.ImageField(upload_to=settings.TOPIC_IMAGE_PATH)

    def __unicode__(self):
        return "Topic Image"

    class Meta:
        verbose_name = u'话题图片'
        verbose_name_plural = u'话题图片'
        db_table = 'image_topic'

    def get_topic_image_url(self):
        path = self.image.path
        url = '/' + '/'.join(path.split('/')[3:])
        return url

    def get_topic_image_name(self):
        name = self.image.name.split('/')[-1]
        return name


class Topic(models.Model):
    """
    话题表
    字段:
    name            名称
    content         内容
    group           所在小组
    creator         创建人
    create_time     创建时间
    modify_time     修改时间
    is_closed       是否已经关闭
    is_top          是否置顶
    ilike           喜欢
    dislike         不喜欢
    last_reply_add  最新回复时间
    reply_amount    回复总数
    image           图片
    click_amount    点击次数
    status          状态
    
    #add by lazytiger
    topic_type      话题类型 : 1类是系统自动发布的，没有作者 ，另一类是用户发表的，需要有作者
    """
    name = models.CharField(max_length=1024, verbose_name=u'名称')
    content = models.TextField(verbose_name=u'内容')
    group = models.ForeignKey(Group, related_name='group_topic', verbose_name=u'小组')
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='creator_topic', verbose_name=u'创建者')
    create_time = models.DateTimeField(default=datetime.datetime.now, verbose_name=u'创建时间')
    modify_time = models.DateTimeField(default=datetime.datetime.now, verbose_name=u'修改时间')
    is_closed = models.BooleanField(default=False, verbose_name=u'话题是否被关闭')
    is_top = models.BooleanField(default=False, verbose_name=u'是否置顶')
    ilike = models.IntegerField(default=0, verbose_name=u'顶')
    dislike = models.IntegerField(default=0, verbose_name=u'踩')
    last_reply_add = models.DateTimeField(default=datetime.datetime.now, verbose_name=u'最新回复时间')
    reply_amount = models.IntegerField(default=0, verbose_name=u'回复总数')
    image = models.ManyToManyField(TopicImage, null=True, blank=True)
    click_amount = models.FloatField(default=1, verbose_name=u'点击数')
    status = models.CharField(verbose_name=u'状态', default='enabled', max_length=56, choices=STATUS_CHOICES)

    topic_type = models.IntegerField(default=0, verbose_name=u'话题类型')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u'话题'
        verbose_name_plural = u'话题'
        db_table = 'topic'

    def save(self, *args, **kwargs):
        self.group.last_topic_add = datetime.datetime.now()  # 更新“最新话题添加时间”
        self.group.topic_amount += 1  # 小组话题数+1
        self.group.save()
        super(Topic, self).save(*args, **kwargs)


class Reply(models.Model):
    """
    回复表
    字段:
    content     回复内容
    creator     创建者
    topic       话题
    reply       回复
    create_time 创建时间
    status      状态
    """
    content = models.TextField(verbose_name=u'内容')
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='creator_reply', verbose_name=u'创建者')
    topic = models.ForeignKey(Topic, related_name='topic_replies', verbose_name=u'话题')
    create_time = models.DateTimeField(default=datetime.datetime.now, verbose_name=u'创建时间')
    reply = models.ForeignKey('self', related_name='reply_reply', null=True, blank=True)
    status = models.CharField(verbose_name=u'状态', default='enabled', max_length=56, choices=STATUS_CHOICES)

    def __unicode__(self):
        return "%s's reply" % self.topic.name

    class Meta:
        verbose_name = u'回应'
        verbose_name_plural = u'回应'
        db_table = 'reply'

    def save(self, *args, **kwargs):
        self.topic.last_reply_add = datetime.datetime.now()  # 更新"话题的最新回复时间"
        self.topic.reply_amount += 1        # 话题回复数量+1
        self.topic.save()
        super(Reply, self).save(*args, **kwargs)


class Report(models.Model):
    """
    举报表
    字段:
    report_type   举报类型
    topic         话题
    reply         回复
    user          用户
    reason        原因
    is_handle     处理情况
    """
    report_type = models.CharField(max_length=128, choices=REPORT_TYPE_CHOICES, verbose_name=u'举报类型')
    topic = models.ForeignKey(Topic, related_name='topic_report', null=True, blank=True)
    reply = models.ForeignKey(Reply, related_name='reply_report', null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_report')
    reason = models.TextField(verbose_name=u'举报原因')
    is_handle = models.BooleanField(default=False, verbose_name=u'处理情况')

    def __unicode__(self):
        return self.topic

    class Meta:
        verbose_name = u'举报'
        verbose_name_plural = u'举报'
        db_table = 'report'



APPLY_STATUS = (('processing', u'处理中'), ('pass', u'通过'), ('rejected', u'未通过'))


class Applicant(models.Model):
    """
    `用户申请加入群组表(group_type为private的群组加入需要通过申请)`
    applicant    申请人
    group        申请加入的小组
    reason       申请理由
    status       状态(处理中,通过,未通过)(processing,pass,rejected)
    join_type         类型(加入群组,群组管理员)(member,manager)
    """
    applicant = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='applicant_user', verbose_name=u'申请人')
    group = models.ForeignKey(Group, related_name='apply_group', verbose_name=u'申请加入的小组')
    reason = models.TextField(verbose_name=u'理由', blank=True, null=True)
    apply_time = models.DateTimeField(verbose_name=u'申请时间', auto_now_add=True)
    status = models.CharField(max_length=256, default='processing', verbose_name=u'状态')
    join_type = models.CharField(max_length=128, verbose_name=u'类型')

    def __unicode__(self):
        return self.applicant

    class Meta:
        verbose_name = u'申请加入群组/成为管理员'
        verbose_name_plural = u'申请加入群组/成为管理员'
        db_table = 'applicant'