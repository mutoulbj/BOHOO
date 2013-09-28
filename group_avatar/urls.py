try:
    from django.conf.urls import patterns, url
except ImportError:
    # Django < 1.4
    from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('group_avatar.views',
                       url(r'^group_add/(?P<group_id>\d+)/$', 'group_add', name='group_avatar_add'),
                       url(r'^group_change/(?P<group_id>\d+)/$', 'group_change', name='group_avatar_change'),
                       url(r'^group_delete/(?P<group_id>\d+)/$', 'group_delete', name='group_avatar_delete'),
                       url(r'^group_render_primary/(?P<group>[\w\d\.\-_]{3,30})/(?P<size>[\d]+)/$',
                           'group_render_primary', name='group_avatar_render_primary'),
                       url(r'^group_list/(?P<group_name>[\+\w\@\.]+)/$', 'group_avatar_gallery',
                           name='group_avatar_gallery'),
                       url(r'^group_list/(?P<group_name>[\+\w\@\.]+)/(?P<id>[\d]+)/$', 'group_avatar',
                           name='group_avatar'),
                       )
