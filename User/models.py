#coding=utf-8
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.template.loader import render_to_string
import datetime
from django.utils import timezone
import utils
from groups.models import Catelog

from django.contrib.auth.models import (
	BaseUserManager, AbstractBaseUser,PermissionsMixin 
)


class MyUserManager(BaseUserManager):
	def create_user(self, email, nickname,user_groups=None,image=None, password=None):
		"""
		Creates and saves a User with the given email, nickname,user_groups image and password.
		"""
		if not email:

			raise ValueError('Users must have an email address')

		if not nickname:
			raise ValueError('Users must have an nickname')
			
		user = self.model(
			email=MyUserManager.normalize_email(email),
			#date_of_birth=date_of_birth,
			nickname=nickname,
			user_groups=user_groups,
			image=image,
		)

		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, email, nickname, password):
		"""
		Creates and saves a User with the given email, nickname,user_groups image and password.
		"""
		user = self.create_user(email,
			password=password,
			#date_of_birth=date_of_birth
			nickname=nickname,
			#user_groups=user_groups,
		)
		user.is_admin = True
		user.is_superuser = True
		user.save(using=self._db)
		return user


class MyUser(AbstractBaseUser,PermissionsMixin):
	email = models.EmailField(
		verbose_name='email address',
		max_length=255,
		unique=True,
		db_index=True,
	)
	#date_of_birth = models.DateField()
	nickname = models.CharField(max_length=100, verbose_name='username',unique=True,db_index=True)
	sign     = models.CharField(max_length=255,verbose_name='签名',null=True,blank=True)
	ipaddr   = models.IPAddressField(verbose_name='注册ip',null=True,blank=True)
	iplocation=models.CharField(max_length=50,verbose_name='注册ip位置',null=True,blank=True)
	job       = models.ForeignKey(Catelog,verbose_name='职业',null=True, blank=True, default = None)
	user_groups = models.CharField(max_length=255, null=True,verbose_name='用户的小组')
	activation_key = models.CharField(_('activation key'), max_length=40,blank=True) 
	date_joined = models.DateTimeField('注册时间', default=timezone.now())
	image = models.ImageField(upload_to='user_images/%Y/%m/%d', blank=True, null=True, verbose_name='小组图片')
	is_active = models.BooleanField(default=True)
	is_admin = models.BooleanField(default=False)

	objects = MyUserManager()

	USERNAME_FIELD = 'nickname'
	REQUIRED_FIELDS = ['email']

	def get_full_name(self):
		# The user is identified by their email address
		return self.nickname

	def get_short_name(self):
		# The user is identified by their email address
		return self.nickname

	def __unicode__(self):
		return self.nickname

	def has_perm(self, perm, obj=None):
		"Does the user have a specific permission?"
		# Simplest possible answer: Yes, always
		return True

	def has_module_perms(self, app_label):
		"Does the user have permissions to view the app `app_label`?"
		# Simplest possible answer: Yes, always
		return True

	@property
	def is_staff(self):
		"Is the user a member of staff?"
		# Simplest possible answer: All admins are staff
		return self.is_admin
		
	def send_activation_email(self,usermail,site):
		ctx_dict = {'activation_key':self.activation_key,
					'expiration_days':settings.ACCOUNT_ACTIVATION_DAYS,'site':site}
		subject = render_to_string('accounts/activation_email_subject.txt',ctx_dict)
		subject = ''.join(subject.splitlines())
		message = render_to_string('accounts/activation_email.txt',ctx_dict)
		#self.email_user(subject,message,settings.DEFAULT_FROM_EMAIL)
		mail = utils.WebSMTP(settings.EMAIL_HOST_USER,settings.EMAIL_HOST_PASSOWORD)
		mail.sendmail(usermail,subject,message)
		
	def activation_key_expired(self):
		expiration_date = datetime.timedelta(days=settings.ACCOUNT_ACTIVATION_DAYS)
		return self.activation_key == u"ALREADY_ACTIVATED" or (self.date_joined + expiration_date <= timezone.now()) 
		
	