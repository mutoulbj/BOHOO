from django.conf.urls import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

# from notification.views import *
urlpatterns = patterns(
    '',
    url(r'^$', 'Bohoo.views.index', name='index'),
    url(r'^avatar/', include('avatar.urls')),
    url(r'^group_avatar/', include('group_avatar.urls')),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^people/', include('User.urls')),
    url(r'^accounts/activate/(?P<activation_key>\w+)/$', 'groups.views.activate'),
    url(r'^accounts/wait_activate/$', 'groups.views.wait_activate'),
    url(r'^group/', include('groups.urls')),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    # url(r"^settings/$", notice_settings, name="notification_notice_settings"),
)
urlpatterns += patterns('',
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)
