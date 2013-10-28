# -*- coding:utf-8 -*-
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import render, redirect
from django.utils import six
from django.utils.translation import ugettext as _

from django.contrib import messages
from django.contrib.auth.decorators import login_required

from group_avatar.forms import PrimaryGroupAvatarForm, DeleteGroupAvatarForm, UploadGroupAvatarForm
from group_avatar.models import GroupAvatar
from group_avatar.settings import GROUP_AVATAR_MAX_AVATARS_PER_USER, GROUP_AVATAR_DEFAULT_SIZE
from group_avatar.signals import group_avatar_updated
from group_avatar.util import (get_primary_group_avatar, get_default_group_avatar_url, get_group)

from groups.models import Group


def _get_next(request):
    """
    The part that's the least straightforward about views in this module is how they
    determine their redirects after they have finished computation.

    In short, they will try and determine the next place to go in the following order:

    1. If there is a variable named ``next`` in the *POST* parameters, the view will
    redirect to that variable's value.
    2. If there is a variable named ``next`` in the *GET* parameters, the view will
    redirect to that variable's value.
    3. If Django can determine the previous page from the HTTP headers, the view will
    redirect to that previous page.
    """
    next = request.POST.get('next', request.GET.get('next',
        request.META.get('HTTP_REFERER', None)))
    if not next:
        next = request.path
    return next


def _get_group_avatars(group):
    # Default set. Needs to be sliced, but that's it. Keep the natural order.
    group_avatars = group.groupavatar_set.all()

    # Current avatar
    primary_group_avatar = group_avatars.order_by('-primary')[:1]
    if primary_group_avatar:
        group_avatar = primary_group_avatar[0]
    else:
        group_avatar = None

    if GROUP_AVATAR_MAX_AVATARS_PER_USER == 1:
        group_avatars = primary_group_avatar
    else:
        # Slice the default set now that we used the queryset for the primary avatar
        group_avatars = group_avatars[:GROUP_AVATAR_MAX_AVATARS_PER_USER]
    return (group_avatar, group_avatars)


@login_required
def group_add(request, group_id, extra_context=None, next_override=None,
        upload_form=UploadGroupAvatarForm, *args, **kwargs):
    group = Group.objects.get(id=group_id)
    if extra_context is None:
        extra_context = {}
    group_avatar, group_avatars = _get_group_avatars(group)
    upload_group_avatar_form = upload_form(request.POST or None,
        request.FILES or None, group=group)
    if request.method == "POST" and 'group_avatar' in request.FILES:
        if upload_group_avatar_form.is_valid():
            group_avatar = GroupAvatar(group=group, primary=True)
            image_file = request.FILES['group_avatar']
            group_avatar.group_avatar.save(image_file.name, image_file)
            group_avatar.save()
            messages.success(request, _("Successfully uploaded a new avatar."))
            group_avatar_updated.send(sender=GroupAvatar, group=group, group_avatar=group_avatar)
            # return redirect(next_override or _get_next(request))
            return redirect(reverse('group_detail', kwargs={'group_id': group.id}) + '?type=recent')
    context = {
        'group': group,
        'group_avatar': group_avatar,
        'group_avatars': group_avatars,
        'upload_group_avatar_form': upload_group_avatar_form,
        'next': next_override or _get_next(request),
    }
    context.update(extra_context)
    return render(request, 'group_avatar/add.html', context)


@login_required
def group_change(request, group_id, extra_context=None, next_override=None,
           upload_form=UploadGroupAvatarForm, primary_form=PrimaryGroupAvatarForm, *args, **kwargs):
    """ 需要传入 group_id 变量 """
    group = Group.objects.get(id=group_id)
    if extra_context is None:
        extra_context = {}
    group_avatar, group_avatars = _get_group_avatars(group)
    if group_avatar:
        kwargs = {'initial': {'choice': group_avatar.id}}
    else:
        kwargs = {}
    upload_group_avatar_form = upload_form(group=group, **kwargs)
    primary_group_avatar_form = primary_form(request.POST or None, group=group, group_avatars=group_avatars, **kwargs)
    if request.method == "POST":
        updated = False
        if 'choice' in request.POST and primary_group_avatar_form.is_valid():
            group_avatar = GroupAvatar.objects.get(
                id=primary_group_avatar_form.cleaned_data['choice'])
            group_avatar.primary = True
            group_avatar.save()
            updated = True
            messages.success(request, _("Successfully updated your avatar."))
        if updated:
            group_avatar_updated.send(sender=GroupAvatar, group=group, group_avatar=group_avatar)
        # TODO: 修改小组头像后跳转
        # return redirect(next_override or _get_next(request))
        return redirect(reverse('group_detail', kwargs={'group_id': group.id}) + '?type=recent')
    context = {
        'group': group,
        'group_avatar': group_avatar,
        'group_avatars': group_avatars,
        'upload_group_avatar_form': upload_group_avatar_form,
        'primary_group_avatar_form': primary_group_avatar_form,
        'next': next_override or _get_next(request)
    }
    context.update(extra_context)
    return render(request, 'group_avatar/change.html', context)


@login_required
def group_delete(request, group_id, extra_context=None, next_override=None, *args, **kwargs):
    group = Group.objects.get(id=group_id)
    if extra_context is None:
        extra_context = {}
    group_avatar, group_avatars = _get_group_avatars(group)
    delete_group_avatar_form = DeleteGroupAvatarForm(request.POST or None, group=group, group_avatars=group_avatars)
    if request.method == 'POST':
        if delete_group_avatar_form.is_valid():
            ids = delete_group_avatar_form.cleaned_data['choices']
            if six.text_type(group_avatar.id) in ids and group_avatars.count() > len(ids):
                # Find the next best avatar, and set it as the new primary
                for a in group_avatars:
                    if six.text_type(a.id) not in ids:
                        a.primary = True
                        a.save()
                        group_avatar_updated.send(sender=GroupAvatar, group=group, group_avatar=group_avatar)
                        break
            GroupAvatar.objects.filter(id__in=ids).delete()
            messages.success(request, _("Successfully deleted the requested avatars."))
            # TODO: 成功删除小组头像后页面跳转
            # return redirect(next_override or _get_next(request))
            return redirect(reverse('group_detail', kwargs={'group_id': group.id}) + '?type=recent')
    context = {
        'group_avatar': group_avatar,
        'group_avatars': group_avatars,
        'group': group,
        'delete_group_avatar_form': delete_group_avatar_form,
        'next': next_override or _get_next(request),
    }
    context.update(extra_context)

    return render(request, 'group_avatar/confirm_delete.html', context)


def group_avatar_gallery(request, group_name, template_name="group_avatar/gallery.html"):
    try:
        group = get_group(group_name)
    except Group.DoesNotExist:
        raise Http404
    return render(request, template_name, {
        "other_group": group,
        "group_avatars": group.groupavatar_set.all(),
    })


def group_avatar(request, group_name, id, template_name="group_avatar/avatar.html"):
    try:
        group = get_group(group_name)
    except Group.DoesNotExist:
        raise Http404
    group_avatars = group.groupavatar_set.order_by("-date_uploaded")
    index = None
    group_avatar = None
    if group_avatars:
        group_avatar = group_avatars.get(pk=id)
        if not group_avatar:
            return Http404

        index = group_avatars.filter(date_uploaded__gt=group_avatar.date_uploaded).count()
        count = group_avatars.count()

        if index == 0:
            prev = group_avatars.reverse()[0]
            if count <= 1:
                next = group_avatars[0]
            else:
                next = group_avatars[1]
        else:
            prev = group_avatars[index - 1]

        if (index + 1) >= count:
            next = group_avatars[0]
            prev_index = index - 1
            if prev_index < 0:
                prev_index = 0
            prev = group_avatars[prev_index]
        else:
            next = group_avatars[index + 1]

    return render(request, template_name, {
        "other_group": group,
        "group_avatar": group_avatar,
        "index": index + 1,
        "group_avatars": group_avatars,
        "next": next,
        "prev": prev,
        "count": count,
    })


def group_render_primary(request, extra_context={}, group=None, size=GROUP_AVATAR_DEFAULT_SIZE, *args, **kwargs):
    size = int(size)
    group_avatar = get_primary_group_avatar(group, size=size)
    if group_avatar:
        # FIXME: later, add an option to render the resized avatar dynamically
        # instead of redirecting to an already created static file. This could
        # be useful in certain situations, particulary if there is a CDN and
        # we want to minimize the storage usage on our static server, letting
        # the CDN store those files instead
        return redirect(group_avatar.avatar_url(size))
    else:
        return redirect(get_default_group_avatar_url())
