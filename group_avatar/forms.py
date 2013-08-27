import os

from django import forms
from django.forms import widgets
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import filesizeformat

from group_avatar.models import GroupAvatar
from group_avatar.settings import (GROUP_AVATAR_MAX_AVATARS_PER_USER, GROUP_AVATAR_MAX_SIZE,
                             GROUP_AVATAR_ALLOWED_FILE_EXTS, GROUP_AVATAR_DEFAULT_SIZE)


def group_avatar_img(group_avatar, size):
    if not group_avatar.thumbnail_exists(size):
        group_avatar.create_thumbnail(size)
    return mark_safe('<img src="%s" alt="%s" width="%s" height="%s" />' %
                     (group_avatar.group_avatar_url(size), group_avatar, size, size))


class UploadGroupAvatarForm(forms.Form):

    group_avatar = forms.ImageField(label=_("group_avatar"))

    def __init__(self, *args, **kwargs):
        self.group = kwargs.pop('group')
        super(UploadGroupAvatarForm, self).__init__(*args, **kwargs)

    def clean_group_avatar(self):
        data = self.cleaned_data['group_avatar']
        if GROUP_AVATAR_ALLOWED_FILE_EXTS:
            (root, ext) = os.path.splitext(data.name.lower())
            if ext not in GROUP_AVATAR_ALLOWED_FILE_EXTS:
                raise forms.ValidationError(
                    _("%(ext)s is an invalid file extension. "
                      "Authorized extensions are : %(valid_exts_list)s") %
                    {'ext': ext, 'valid_exts_list': ", ".join(GROUP_AVATAR_ALLOWED_FILE_EXTS)})
        if data.size > GROUP_AVATAR_MAX_SIZE:
            error = _("Your file is too big (%(size)s), "
                      "the maximum allowed size is %(max_valid_size)s")
            raise forms.ValidationError(error % {
                'size': filesizeformat(data.size),
                'max_valid_size': filesizeformat(GROUP_AVATAR_MAX_SIZE)
            })

        count = GroupAvatar.objects.filter(group=self.group).count()
        if GROUP_AVATAR_MAX_AVATARS_PER_USER > 1 and count >= GROUP_AVATAR_MAX_AVATARS_PER_USER:
            error = _("You already have %(nb_avatars)d avatars, "
                      "and the maximum allowed is %(nb_max_avatars)d.")
            raise forms.ValidationError(error % {
                'nb_avatars': count,
                'nb_max_avatars': GROUP_AVATAR_MAX_AVATARS_PER_USER,
            })
        return


class PrimaryGroupAvatarForm(forms.Form):

    def __init__(self, *args, **kwargs):
        kwargs.pop('group')
        size = kwargs.pop('size', GROUP_AVATAR_DEFAULT_SIZE)
        group_avatars = kwargs.pop('group_avatars')
        super(PrimaryGroupAvatarForm, self).__init__(*args, **kwargs)
        self.fields['choice'] = forms.ChoiceField(label=_("Choices"),
            choices=[(c.id, group_avatar_img(c, size)) for c in group_avatars],
            widget=widgets.RadioSelect)


class DeleteGroupAvatarForm(forms.Form):

    def __init__(self, *args, **kwargs):
        kwargs.pop('group')
        size = kwargs.pop('size', GROUP_AVATAR_DEFAULT_SIZE)
        group_avatars = kwargs.pop('group_avatars')
        super(DeleteGroupAvatarForm, self).__init__(*args, **kwargs)
        self.fields['choices'] = forms.MultipleChoiceField(label=_("Choices"),
            choices=[(c.id, group_avatar_img(c, size)) for c in group_avatars],
            widget=widgets.CheckboxSelectMultiple)
