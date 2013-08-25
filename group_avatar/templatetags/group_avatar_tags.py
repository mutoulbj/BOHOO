import hashlib

try:
    from urllib.parse import urljoin, urlencode
except ImportError:
    from urlparse import urljoin
    from urllib import urlencode

from django import template
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string
from django.utils import six
from django.utils.translation import ugettext as _

try:
    from django.utils.encoding import force_bytes
except ImportError:
    force_bytes = str

from group_avatar.settings import (GROUP_AVATAR_GRAVATAR_BACKUP, GROUP_AVATAR_GRAVATAR_DEFAULT,
                             GROUP_AVATAR_DEFAULT_SIZE, GROUP_AVATAR_GRAVATAR_BASE_URL)
from group_avatar.util import (get_primary_group_avatar, get_default_group_avatar_url,
                         cache_result, get_group)
from group_avatar.models import GroupAvatar
from groups.models import Group

register = template.Library()


@cache_result
@register.simple_tag
def group_avatar_url(group, size=GROUP_AVATAR_DEFAULT_SIZE):
    group_avatar = get_primary_group_avatar(group, size=size)
    if group_avatar:
        return group_avatar.group_avatar_url(size)

    if GROUP_AVATAR_GRAVATAR_BACKUP:
        params = {'s': str(size)}
        if GROUP_AVATAR_GRAVATAR_DEFAULT:
            params['d'] = GROUP_AVATAR_GRAVATAR_DEFAULT
        path = "%s/?%s" % (hashlib.md5(force_bytes(group.name)).hexdigest(),
                           urlencode(params))
        return urljoin(GROUP_AVATAR_GRAVATAR_BASE_URL, path)

    return get_default_group_avatar_url()


@cache_result
@register.simple_tag
def group_avatar(group, size=GROUP_AVATAR_DEFAULT_SIZE, **kwargs):
    if not isinstance(group, Group):
        try:
            group = get_group(group)
            alt = six.text_type(group)
            url = group_avatar_url(group, size)
        except Group.DoesNotExist:
            url = get_default_group_avatar_url()
            alt = _("Default Group Avatar")
    else:
        alt = six.text_type(group)
        url = group_avatar_url(group, size)
    context = dict(kwargs, **{
        'group': group,
        'url': url,
        'alt': alt,
        'size': size,
    })
    return render_to_string('group_avatar/group_avatar_tag.html', context)


@register.filter
def has_group_avatar(group):
    if not isinstance(group, Group):
        return False
    return GroupAvatar.objects.filter(group=group, primary=True).exists()


@cache_result
@register.simple_tag
def primary_group_avatar(group, size=GROUP_AVATAR_DEFAULT_SIZE):
    """
    This tag tries to get the default avatar for a user without doing any db
    requests. It achieve this by linking to a special view that will do all the
    work for us. If that special view is then cached by a CDN for instance,
    we will avoid many db calls.
    """
    alt = six.text_type(group)
    url = reverse('group_avatar_render_primary', kwargs={'group': group, 'size': size})
    return """<img src="%s" alt="%s" width="%s" height="%s" />""" % (url, alt,
        size, size)


@cache_result
@register.simple_tag
def render_group_avatar(group_avatar, size=GROUP_AVATAR_DEFAULT_SIZE):
    if not group_avatar.thumbnail_exists(size):
        group_avatar.create_thumbnail(size)
    return """<img src="%s" alt="%s" width="%s" height="%s" />""" % (
        group_avatar.group_avatar_url(size), str(group_avatar), size, size)


@register.tag
def primary_group_avatar_object(parser, token):
    split = token.split_contents()
    if len(split) == 4:
        return GroupAvatarObjectNode(split[1], split[3])
    else:
        raise template.TemplateSyntaxError('%r tag takes three arguments.' % split[0])


class GroupAvatarObjectNode(template.Node):
    def __init__(self, group, key):
        self.group = template.Variable(group)
        self.key = key

    def render(self, context):
        group = self.group.resolve(context)
        key = self.key
        group_avatar = GroupAvatar.objects.filter(group=group, primary=True)
        if group_avatar:
            context[key] = group_avatar[0]
        else:
            context[key] = None
        return six.text_type()
