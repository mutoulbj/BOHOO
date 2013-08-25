from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from group_avatar.models import GroupAvatar
from group_avatar.signals import group_avatar_updated
from group_avatar.templatetags.group_avatar_tags import group_avatar
from groups.models import Group


class GroupAvatarAdmin(admin.ModelAdmin):
    list_display = ('get_group_avatar', 'group', 'primary', "date_uploaded")
    list_filter = ('primary',)
    search_fields = ('user__%s' % getattr(Group, 'GROUP_NAME_FIELD', 'group_name'),)
    list_per_page = 50

    def get_group_avatar(self, group_avatar_in):
        return group_avatar(group_avatar_in.group, 80)

    get_group_avatar.short_description = _('Group Avatar')
    get_group_avatar.allow_tags = True

    def save_model(self, request, group, obj, form, change):
        super(GroupAvatarAdmin, self).save_model(request, obj, form, change)
        group_avatar_updated.send(sender=GroupAvatar, group=group, group_avatar=obj)


admin.site.register(GroupAvatar, GroupAvatarAdmin)
