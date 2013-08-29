from django.conf.urls import patterns, include, url

# urlpatterns = patterns(
#     'groups.views',
#     url(r'^guide/$', 'guide', name='guide'),
#     url(r'^explore/$', 'home', name='home'),
#     url(r'^explore_topic/$', 'explore_topic', name='explore_topic'),
#     url(r'^mygroup/$', 'mygroup', name='mygroup'),
#     url(r'^my_topics/$', 'my_topics', name='my_topics'),
#     url(r'^my_replied_topics/$', 'my_replied_topics', name='my_replied_topics'),
#     url(r'^mine/$', 'mine', name='mine'),
#     url(r'^join/$', 'groupjoin', name='groupjoin'),
#     url(r'^new_group/$', 'new_group', name='new_group'),
#     url(r'^(?P<gname>(.*?))/new_topic/$', 'new_topic', name='new_topic'),
#     url(r'^get_captcha/$', 'get_captcha', name='get_captcha'),
#     url(r'^search/$', 'search', name='search'),
#     url(r'^topic/(?P<id>\d+)/$', 'topic', name='topic'),
#     url(r'^topic/(?P<id>\d+)/remove_comment/$', 'remove_comment', name='remove_comment'),
#     url(r'^topic/(?P<id>\d+)/admin_remove/$', 'admin_remove', name='admin_remove'),
#     url(r'^show/(?P<gname>(.*?))/$', 'showgroup', name='showgroup'),
#     url(r'^topic/add_comment/(\d+)$', 'add_comment', name='add_comment'),
#     url(r'^(?P<gname>(.*?))/group_edit/$', 'group_edit', name='group_edit'),
#     url(r'^(?P<gname>(.*?))/members/$', 'members', name='members'),
#     url(r'^(?P<gname>(.*?))/advance/$', 'advance', name='advance'),
#     url(r'^add_friendgroup/$', 'add_friendgroup', name='add_friendgroup'),
#     url(r'^change_privacy/$', 'change_privacy', name='change_privacy'),
#     url(r'^change_join/$', 'change_join', name='change_join'),
#     url(r'^user_report/$', 'user_report', name='user_report'),
#     url(r'^upload-images/$', 'upload_images', name='upload_images'),
#     url(r'^del_image/$', 'del_image', name='del_image'),
#     url(r'^(.*?).htm/$', 'dispatcher', name='dispatcher'),
# )

urlpatterns = patterns(
    'groups.views',
    url(r'^my_groups/$', 'my_groups', name='my_groups'),
    url(r'^new_group/$', 'new_group', name='new_group'),
    url(r'^add_avatar/(?P<group_id>\d+)/$', 'add_group_avatar', name='add_group_avatar'),
    url(r'^group/detail/(?P<group_id>\d+)/$', 'group_detail', name='group_detail'),
    url(r'^ajax_join_group/$', 'ajax_join_group', name='ajax_join_group')
)
