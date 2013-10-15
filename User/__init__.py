from User.signals import myuser_logged_in


def after_login_callback(sender, user, request, **kwargs):
    import datetime
    if user:
        user.latest_login = datetime.datetime.now()
        user.save()

myuser_logged_in.connect(after_login_callback, dispatch_uid="update_lastest_login")