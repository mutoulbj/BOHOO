#! -*- coding:utf-8 -*-
from django.conf.urls import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

# from notification.views import *
urlpatterns = patterns(
    '',
    url(r'^$', 'Bohoo.views.main', name='main'),
    url(r'^home/$', 'Bohoo.views.index', name='index'),
    url(r'^contact/$', 'Bohoo.views.contact', name='contact_us'),     # 联系我们
    url(r'^statement/$', 'Bohoo.views.statement', name='statement'),  # 免责声明
    url(r'^about/$', 'Bohoo.views.about', name='about'),       # 关于页面
    url(r'^terms/$', 'Bohoo.views.terms', name='terms'),       # 服务条款
    url(r'^get_messages/$', 'Bohoo.views.get_messages', name='get_messages'),   # 轮询
    url(r'^captcha/', include('captcha.urls')),   # django-simple-captcha
    url(r'^search/$', 'Bohoo.views.search', name='search'),
    url(r'^avatar/', include('avatar.urls')),
    url(r'^group_avatar/', include('group_avatar.urls')),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^accounts/', include('social.urls')),
    url(r'^people/', include('User.urls')),
    url(r'^group/', include('groups.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
#     url(r'^admin/check_weibo_auth/$', 'blog.admin_views.check_weibo_auth'),
#     url(r'^admin/weibo/auth/$', 'blog.admin_views.admin_weibo_auth'),
#     url(r'^admin/weibo/auth/done/$', 'blog.admin_views.admin_weibo_auth_deal'),
    url(r'^group/', include('groups.urls')),
    
    url(r'^friends/', include('friends.urls')),
    url(r'^message/', include('django_messages.urls')),
    url(r'^notification/', include('sys_notification.urls'))
    
    # url(r"^settings/$", notice_settings, name="notification_notice_settings"),
)
urlpatterns += patterns('',
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)
