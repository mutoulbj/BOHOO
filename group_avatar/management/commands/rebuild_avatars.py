from django.core.management.base import NoArgsCommand

from group_avatar.models import GroupAvatar
from group_avatar.settings import GROUP_AUTO_GENERATE_AVATAR_SIZES


class Command(NoArgsCommand):
    help = ("Regenerates avatar thumbnails for the sizes specified in "
            "settings.AUTO_GENERATE_AVATAR_SIZES.")

    def handle_noargs(self, **options):
        for group_avatar in GroupAvatar.objects.all():
            for size in GROUP_AUTO_GENERATE_AVATAR_SIZES:
                print("Rebuilding Group Avatar id=%s at size %s." % (group_avatar.id, size))
                group_avatar.create_thumbnail(size)
