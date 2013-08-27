import django.dispatch


group_avatar_updated = django.dispatch.Signal(providing_args=["group", "group_avatar"])
