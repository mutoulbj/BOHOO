# -*- coding:utf-8 -*-
import datetime
import os
import hashlib
from PIL import Image

from django.conf import settings
from django.db import models
from django.core.files.base import ContentFile
from django.core.files.storage import get_storage_class
from django.utils.translation import ugettext as _
from django.utils import six
from django.db.models import signals

try:
    from django.utils.encoding import force_bytes
except ImportError:
    force_bytes = str

from group_avatar.util import get_group_name

try:
    from django.utils.timezone import now
except ImportError:
    now = datetime.datetime.now

from group_avatar.util import invalidate_cache
from group_avatar.settings import (GROUP_AVATAR_STORAGE_DIR, GROUP_AVATAR_RESIZE_METHOD,
                             GROUP_AVATAR_MAX_AVATARS_PER_USER, GROUP_AVATAR_THUMB_FORMAT,
                             GROUP_AVATAR_HASH_USERDIRNAMES, GROUP_AVATAR_HASH_FILENAMES,
                             GROUP_AVATAR_THUMB_QUALITY, GROUP_AUTO_GENERATE_AVATAR_SIZES,
                             GROUP_AVATAR_DEFAULT_SIZE, GROUP_AVATAR_STORAGE,
                             GROUP_AVATAR_CLEANUP_DELETED)

from groups.models import Group

group_avatar_storage = get_storage_class(GROUP_AVATAR_STORAGE)()


def group_avatar_file_path(instance=None, filename=None, size=None, ext=None):
    tmppath = [GROUP_AVATAR_STORAGE_DIR]
    if GROUP_AVATAR_HASH_USERDIRNAMES:
        tmp = hashlib.md5(get_group_name(instance.group)).hexdigest()
        tmppath.extend([tmp[0], tmp[1], get_group_name(instance.group)])
    else:
        tmppath.append(get_group_name(instance.group))
    if not filename:
        # Filename already stored in database
        filename = instance.group_avatar.name
        if ext and GROUP_AVATAR_HASH_FILENAMES:
            # An extension was provided, probably because the thumbnail
            # is in a different format than the file. Use it. Because it's
            # only enabled if AVATAR_HASH_FILENAMES is true, we can trust
            # it won't conflict with another filename
            (root, oldext) = os.path.splitext(filename)
            filename = root + "." + ext
    else:
        # File doesn't exist yet
        if GROUP_AVATAR_HASH_FILENAMES:
            (root, ext) = os.path.splitext(filename)
            filename = hashlib.md5(force_bytes(filename)).hexdigest()
            filename = filename + ext
    # TODO: 下面两行被注释了
    # if size:
    #     tmppath.extend(['resized', str(size)])
    tmppath.append(os.path.basename(filename))
    return os.path.join(*tmppath)


def find_extension(format):
    format = format.lower()

    if format == 'jpeg':
        format = 'jpg'

    return format


class GroupAvatar(models.Model):
    group = models.ForeignKey(Group)
    primary = models.BooleanField(default=False)
    group_avatar = models.ImageField(max_length=1024,
                               upload_to=group_avatar_file_path,
                               storage=group_avatar_storage,
                               blank=True)
    date_uploaded = models.DateTimeField(default=now)

    def __unicode__(self):
        return _(six.u('Group Avatar for %s')) % self.group

    def save(self, *args, **kwargs):
        group_avatars = GroupAvatar.objects.filter(group=self.group)
        if self.pk:
            group_avatars = group_avatars.exclude(pk=self.pk)
        if GROUP_AVATAR_MAX_AVATARS_PER_USER > 1:
            if self.primary:
                group_avatars = group_avatars.filter(primary=True)
                group_avatars.update(primary=False)
        else:
            group_avatars.delete()
        super(GroupAvatar, self).save(*args, **kwargs)

    def thumbnail_exists(self, size):
        return self.group_avatar.storage.exists(self.avatar_name(size))

    def create_thumbnail(self, size, quality=None):
        # invalidate the cache of the thumbnail with the given size first
        invalidate_cache(self.group, size)
        try:
            orig = self.group_avatar.storage.open(self.group_avatar.name, 'rb')
            image = Image.open(orig)
            quality = quality or GROUP_AVATAR_THUMB_QUALITY
            w, h = image.size
            if w != size or h != size:
                if w > h:
                    diff = int((w - h) / 2)
                    image = image.crop((diff, 0, w - diff, h))
                else:
                    diff = int((h - w) / 2)
                    image = image.crop((0, diff, w, h - diff))
                if image.mode != "RGB":
                    image = image.convert("RGB")
                image = image.resize((size, size), GROUP_AVATAR_RESIZE_METHOD)
                thumb = six.BytesIO()
                image.save(thumb, GROUP_AVATAR_THUMB_FORMAT, quality=quality)
                thumb_file = ContentFile(thumb.getvalue())
            else:
                thumb_file = ContentFile(orig)
            thumb = self.group_avatar.storage.save(self.group_avatar_name(size), thumb_file)
        except IOError:
            return  # What should we do here?  Render a "sorry, didn't work" img?

    def group_avatar_url(self, size):
        return self.group_avatar.storage.url(self.group_avatar_name(size))

    def get_absolute_url(self):
        return self.group_avatar_url(GROUP_AVATAR_DEFAULT_SIZE)

    def group_avatar_name(self, size):
        ext = find_extension(GROUP_AVATAR_THUMB_FORMAT)
        return group_avatar_file_path(
            instance=self,
            size=size,
            ext=ext
        )


def invalidate_group_avatar_cache(sender, instance, **kwargs):
    invalidate_cache(instance.group)


def create_default_thumbnails(sender, instance, created=False, **kwargs):
    invalidate_group_avatar_cache(sender, instance)
    if created:
        for size in GROUP_AUTO_GENERATE_AVATAR_SIZES:
            instance.create_thumbnail(size)


def remove_group_avatar_images(instance=None, **kwargs):
    for size in GROUP_AUTO_GENERATE_AVATAR_SIZES:
        if instance.thumbnail_exists(size):
            instance.group_avatar.storage.delete(instance.group_avatar_name(size))
    instance.avatar.storage.delete(instance.avatar.name)


signals.post_save.connect(create_default_thumbnails, sender=GroupAvatar)
signals.post_delete.connect(invalidate_group_avatar_cache, sender=GroupAvatar)

if GROUP_AVATAR_CLEANUP_DELETED:
    signals.post_delete.connect(remove_group_avatar_images, sender=GroupAvatar)
