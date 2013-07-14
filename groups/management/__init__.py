#coding:utf-8
from django.db.models.signals import post_syncdb
import groups.models
from groups.models import *

from User.models import MyUser

def Groups_init(sender, **kwargs):
    # Your specific logic here
    print "lalallalalallalallalallaa"
    Catelog.objects.create(cate_name = "互联网",parent_id = -1)
    Catelog.objects.create(cate_name = "软件",parent_id = 1)
    Catelog.objects.create(cate_name = "产品",parent_id = 1)
    for i in range(0,110):
        Group.objects.create(name = 'Group %d'%i,description= 'This is Group %d'%i,catelog =Catelog.objects.get(cate_name='杞�欢'),
                                     creator = MyUser.objects.get(nickname='amituofo'),create_time = datetime.datetime.now(),
                                     modify_time=datetime.datetime.now())
        

post_syncdb.connect(Groups_init, sender=groups.models)