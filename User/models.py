#coding=utf-8
import datetime
import utils

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.template.loader import render_to_string
from django.utils import timezone
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin


class MyUserManager(BaseUserManager):
    # 创建用户
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        if not username:
            raise ValueError('Users must have a username')
        if not password:
            raise ValueError('Users must have a password')

        user = self.model(
            email=MyUserManager.normalize_email(email),
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    # 创建超级用户
    def create_superuser(self, email, username, password):
        user = self.create_user(email=email,
                                username=username,
                                password=password
                                )
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser, PermissionsMixin):
    """
    ``用户表``
    email 邮件
    username 用户名
    sign  签名
    job 工作
    activation_key  激活码
    date_joined  注册时间
    avatar  头像
    first_name 名
    last_name 姓
    is_active 允许登录
    is_admin  管理员
    follower  关注者
    sex   性别
    birthday  生日
    country   国家
    state     州省
    city    区县
    qq      qq号码
    weibo   微博帐号
    phone_number  电话号码
    """
    SEX_CHOICES = (('M', u'男'), ('F', u'女'))
    email = models.EmailField(max_length=255, verbose_name=u'邮箱', unique=True, db_index=True)
    username = models.CharField(max_length=100, verbose_name=u'用户名', unique=True, db_index=True)
    sign = models.CharField(max_length=1024, verbose_name=u'签名', null=True, blank=True)
    job = models.CharField(max_length=1024, verbose_name=u'职业', null=True, blank=True, default=None)
    activation_key = models.CharField(max_length=40, verbose_name=u'激活码', blank=True)
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name=u'注册时间')
    # avatar = models.ImageField(upload_to='user_avatar/%Y/%m/%d', blank=True, null=True, verbose_name=u'头像')
    first_name = models.CharField(max_length=256, verbose_name=u'名', null=True, blank=True)
    last_name = models.CharField(max_length=256, verbose_name=u'姓', null=True, blank=True)
    is_active = models.BooleanField(default=True, verbose_name=u'是否允许用户登录')
    is_admin = models.BooleanField(default=False, verbose_name=u'是否管理员')
    follower = models.ManyToManyField('self')
    sex = models.CharField(max_length=128, verbose_name=u'性别', null=True, blank=True, choices=SEX_CHOICES)
    birthday = models.DateField(verbose_name=u'生日', null=True, blank=True)
    country = models.CharField(max_length=256, verbose_name=u'国家', null=True, blank=True)
    state = models.CharField(max_length=256, verbose_name=u'州省', null=True, blank=True)
    city = models.CharField(max_length=256, verbose_name=u'区县', null=True, blank=True)
    qq = models.IntegerField(verbose_name=u'qq', null=True, blank=True)
    weibo = models.CharField(max_length=256, verbose_name=u'微博', null=True, blank=True)
    phone_number = models.CharField(max_length=25, verbose_name=u'手机', null=True, blank=True)
    objects = MyUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def get_full_name(self):
        # 返回全名
        return self.last_name + self.first_name

    def get_short_name(self):
        # 返回名字
        return self.first_name

    def get_username(self):
        # 返回用户名
        return self.username

    def __unicode__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        """Is the user a member of staff?"""
        # Simplest possible answer: All admins are staff
        return self.is_admin

    def send_activation_email(self, usermail, site):
        ctx_dict = {'activation_key': self.activation_key,
                    'expiration_days': settings.ACCOUNT_ACTIVATION_DAYS, 'site': site}
        subject = render_to_string('accounts/activation_email_subject.txt', ctx_dict)
        subject = ''.join(subject.splitlines())
        message = render_to_string('accounts/activation_email.txt', ctx_dict)
        #self.email_user(subject,message,settings.DEFAULT_FROM_EMAIL)
        mail = utils.WebSMTP(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSOWORD)
        mail.sendmail(usermail, subject, message)

    def activation_key_expired(self):
        expiration_date = datetime.timedelta(days=settings.ACCOUNT_ACTIVATION_DAYS)
        return self.activation_key == u"ALREADY_ACTIVATED" or (self.date_joined + expiration_date <= timezone.now())
