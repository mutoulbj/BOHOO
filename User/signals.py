#! -*- coding:utf-8 -*-
from django.dispatch import Signal

myuser_logged_in = Signal(providing_args=['request', 'user'])
# myuser_logged_out = Signal(providing_args=['request', 'user'])