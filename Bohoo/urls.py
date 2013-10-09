from django.conf.urls import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

# from notification.views import *
urlpatterns = patterns(
    '',
    url(r'^$', 'Bohoo.views.index', name='index'),
    url(r'^captcha/', include('captcha.urls')),   # django-simple-captcha
    url(r'^search/$', 'Bohoo.views.search', name='search'),
    url(r'^avatar/', include('avatar.urls')),
    url(r'^group_avatar/', include('group_avatar.urls')),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^accounts/', include('social.urls')),
    url(r'^people/', include('User.urls')),
    url(r'^group/', include('groups.urls')),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
#     url(r'^admin/check_weibo_auth/$', 'blog.admin_views.check_weibo_auth'),
#     url(r'^admin/weibo/auth/$', 'blog.admin_views.admin_weibo_auth'),
#     url(r'^admin/weibo/auth/done/$', 'blog.admin_views.admin_weibo_auth_deal'),
    url(r'^group/', include('groups.urls')),
    
    url(r'^relation/', include('friends.urls')),
    url(r'^message/', include('django_messages.urls')),
    
    # url(r"^settings/$", notice_settings, name="notification_notice_settings"),
)
urlpatterns += patterns('',
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)
