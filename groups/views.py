# Create your views here.
#coding=utf-8
import json
import re
import datetime
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from models import Group, Topic, Reply, Applicant, TopicImage
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.conf import settings

from User.models import MyUser
from groups.forms import group, topicForm, replyForm, topicImageForm


def new_group(request):
    """ 创建群组 @fanlintao """
    if request.method == 'POST':
        form = group(request.POST)
        if form.is_valid():
            g = form.save(commit=False)
            g.creator = request.user
            g.save()
            g.manager.add(request.user)   # 创建者默认是管理员
            g.member.add(request.user)    # 创建者默认是小组成员
            return redirect(reverse("group_detail", args=[g.id]))
    return render(request, 'groups/new/group.html', {'form': group()})


def edit_group(request, group_id):
    """ 修改群组 @fanlintao """
    try:
        t_group = Group.objects.get(id=group_id)
        if request.method == 'POST':
            form = group(request.POST, instance=t_group)
            if form.is_valid():
                g = form.save(commit=False)
                g.modify_time = datetime.datetime.now()
                g.save()
                return redirect(reverse("group_my_manage"))
        return render(request, 'groups/edit.html', {'t_group': t_group, 'form': group(instance=t_group)})
    except ObjectDoesNotExist:
        pass


def add_group_avatar(request, group_id):
    """ 添加小组头像 """
    group = Group.objects.get(id=group_id)
    return render(request, 'groups/new/add_avatar.html', {'group': group})


def group_detail(request, group_id):
    """ 群组详细页 @fanlintao"""
    try:
        group = Group.objects.get(id=group_id)
        is_member, is_manager = False, False
        # 判断当前用户是不是小组成员
        if request.user in group.member.all():
            is_member = True
        # 判断当前用户是不是小组管理员
        if request.user in group.manager.all():
            is_manager = True
        # 判断当前用户申请加入该小组的请求是否正在处理中,若正在处理中,不允许重复申请
        try:
            apply_is_processing = Applicant.objects.get(applicant=request.user, group=group, status="processing",
                                                        join_type="member")
            is_member_processing = True
        except ObjectDoesNotExist:
            is_member_processing = False

        try:
            apply_is_processing = Applicant.objects.get(applicant=request.user, group=group, status="processing",
                                                        join_type="manager")
            is_manager_processing = True
        except ObjectDoesNotExist:
            is_manager_processing = False
        topics = Topic.objects.filter(group=group).order_by("-last_reply_add")
        return render(request, 'groups/detail.html', {'g': group, 'is_member': is_member, 'topics': topics,
                                                      'is_member_processing': is_member_processing,
                                                      'is_manager': is_manager,
                                                      'is_manager_processing': is_manager_processing})
    except ObjectDoesNotExist:
        pass


def ajax_join_group(request):
    """ 加入群组  ajax @fanlintao """
    error = {"success": "", "error": ""}
    if request.method == 'POST':
        group = Group.objects.get(id=request.POST.get("group_id"))
        group.member.add(request.user)
        error["success"] = "success"
        return HttpResponse(json.dumps(error, ensure_ascii=False), mimetype="application/json")


def ajax_apply_join_group(request):
    """ 申请加入群组 ajax @fanlintao """
    error = {"success": "", "error": ""}
    if request.method == 'POST':
        try:
            group = Group.objects.get(id=request.POST.get("group_id"))
            reason = request.POST.get("apply_reason")
            applicant = Applicant(applicant=request.user, group=group, reason=reason, join_type="member")
            applicant.save()
            error["success"] = "success"
            return HttpResponse(json.dumps(error, ensure_ascii=False), mimetype="application/json")
        except ObjectDoesNotExist:
            error["success"] = "error"
            return HttpResponse(json.dumps(error, ensure_ascii=False), mimetype="application/json")


def ajax_apply_be_manager(request):
    """ 申请成为组长 ajax @fanlintao """
    error = {"success": "", "error": ""}
    if request.method == "POST":
        try:
            group = Group.objects.get(id=request.POST.get("group_id"))
            reason = request.POST.get("apply_reason")
            applicant = Applicant(applicant=request.user, group=group, reason=reason, join_type="manager")
            applicant.save()
            error["success"] = "success"
            return HttpResponse(json.dumps(error, ensure_ascii=False), mimetype="application/json")
        except ObjectDoesNotExist:
            error["success"] = "error"
            return HttpResponse(json.dumps(error, ensure_ascii=False), mimetype="application/json")


def ajax_quite_group(request):
    error = {"success": "", "error": ""}
    if request.method == 'POST':
        try:
            group = Group.objects.get(id=request.POST.get("group_id"))
            group.member.remove(request.user)
            if request.user in group.manager.all():  # 如果是管理员,退出时也移除其管理员资格
                group.manager.remove(request.user)
            error["success"] = "success"
            return HttpResponse(json.dumps(error, ensure_ascii=False), mimetype="application/json")
        except ObjectDoesNotExist:
            error["success"] = "error"
            return HttpResponse(json.dumps(error, ensure_ascii=False), mimetype="application/json")


def manage(request):
    """ 我管理的群组 @fanlintao """
    groups = Group.objects.filter(manager=request.user)
    return render(request, 'groups/managed.html', {'groups': groups})


def joined(request):
    """  我加入的群组 @fanlintao """
    groups = Group.objects.filter(member=request.user)
    return render(request, 'groups/joined.html', {'groups': groups})


def apply_deal(request, group_id):
    """ 处理请求 @fanlintao """
    try:
        group = Group.objects.get(id=group_id)
        m_applicant = Applicant.objects.filter(group=group, status="processing", join_type="member")
        g_applicant = Applicant.objects.filter(group=group, status="processing", join_type="manager")
        return render(request, 'groups/apply_deal.html', {'m_applicant': m_applicant, 'g_applicant': g_applicant})
    except ObjectDoesNotExist:
        pass


def ajax_apply_pass(request):
    """ ajax 通过请求 @fanlintao """
    error = {"success": "", "error": ""}
    if request.method == 'POST':
        try:
            pass_type = request.POST.get("type")
            group = Group.objects.get(id=request.POST.get("group_id"))
            user = MyUser.objects.get(id=request.POST.get("applicant_id"))
            applicant = Applicant.objects.get(applicant=user, status="processing")
            if pass_type == "member":
                group.member.add(user)
            elif pass_type == "manager":
                group.manager.add(user)
            applicant.status = 'pass'
            applicant.save()
            error['success'] = 'success'
            return HttpResponse(json.dumps(error, ensure_ascii=False), mimetype="application/json")
        except ObjectDoesNotExist:
            error['error'] = 'error'
            return HttpResponse(json.dumps(error, ensure_ascii=False), mimetype="application/json")


def ajax_apply_reject(request):
    """ ajax 拒绝请求 @fanlintao """
    error = {"success": "", "error": ""}
    if request.method == 'POST':
        try:
            applicant = Applicant.objects.get(id=request.POST.get("applicant_id"), status="processing")
            applicant.status = 'reject'
            applicant.save()
            error['success'] = 'success'
            return HttpResponse(json.dumps(error, ensure_ascii=False), mimetype="application/json")
        except ObjectDoesNotExist:
            error['error'] = 'error'
            return HttpResponse(json.dumps(error, ensure_ascii=False), mimetype="application/json")


image_obj = []
def add_topic(request, group_id):
    """ 添加话题 @fanlintao """
    try:
        group = Group.objects.get(id=group_id)
        global image_obj
        if request.method == 'POST':
            form = topicForm(request.POST)
            if "image" in request.FILES:   # 如果有上传图片
                imageForm = topicImageForm(request.POST, request.FILES)
                if imageForm.is_valid():
                    import ImageFile
                    f = request.FILES["image"]
                    parser = ImageFile.Parser()
                    for chunk in f.chunks():
                        parser.feed(chunk)
                    img = parser.close()
                    img.save(settings.TOPIC_IMAGE_PATH+f.name)
                    i = imageForm.save()
                    image_obj.append(i)
                    print image_obj[0].image
            if form.is_valid():
                g = form.save(commit=False)
                g.creator = request.user
                g.save()
                if len(image_obj):
                    for i in image_obj:
                        g.image.add(i)
                image_obj = []
                g_id = int(group.id)
                return redirect(reverse("group_detail", kwargs={'group_id': g_id}))
        print image_obj
        ctx = {
            'form': topicForm(initial={"group": group}),
            'g': group,
            'imageForm': topicImageForm(),
            'images': image_obj
        }
        return render(request, 'topics/new/topic.html', ctx)
    except ObjectDoesNotExist:
        pass


def edit_topic(request, group_id, topic_id):
    """编辑话题 @fanlintao """
    try:
        group = Group.objects.get(id=group_id)
        t_topic = Topic.objects.get(id=topic_id)
        global image_obj
        for i in t_topic.image.all():
            if i not in image_obj:
                image_obj.append(i)
        if request.method == 'POST':
            form = topicForm(request.POST, instance=t_topic)
            if "image" in request.FILES:   # 如果有上传图片
                imageForm = topicImageForm(request.POST, request.FILES)
                if imageForm.is_valid():
                    import ImageFile
                    f = request.FILES["image"]
                    parser = ImageFile.Parser()
                    for chunk in f.chunks():
                        parser.feed(chunk)
                    img = parser.close()
                    img.save(settings.TOPIC_IMAGE_PATH+f.name)
                    i = imageForm.save()
                    image_obj.append(i)
                    print image_obj[0].image
            if form.is_valid():
                g = form.save(commit=False)
                g.creator = request.user
                g.save()
                if len(image_obj):
                    for i in image_obj:
                        g.image.add(i)
                image_obj = []
                g_id = int(group.id)
                return redirect(reverse("group_detail", kwargs={'group_id': g_id}))
        print image_obj
        ctx = {
            'form': topicForm(instance=t_topic),
            'g': group,
            'imageForm': topicImageForm(),
            'images': image_obj
        }
        return render(request, 'topics/new/topic.html', ctx)
    except ObjectDoesNotExist:
        pass


def ajax_delete_topic_image(request):
    """ 删除图片 @fanlintao """
    error = {"success": "", "error": ""}
    if request.method == 'POST':
        try:
            image = TopicImage.objects.get(id=request.POST.get("image_id"))
            global image_obj
            image_obj.remove(image)
            image.delete()
            error["success"] = "success"
            return HttpResponse(json.dumps(error, ensure_ascii=False), mimetype="application/json")
        except ObjectDoesNotExist:
            error["success"] = "error"
            return HttpResponse(json.dumps(error, ensure_ascii=False), mimetype="application/json")


def group_topic(request):
    """ 最近的话题 @fanlintao """
    groups = Group.objects.filter(member=request.user)
    topics = Topic.objects.filter(group__in=groups).order_by("-last_reply_add")
    return render(request, "topics/group.html", {"topics": topics})


def created_topic(request):
    """我创建的话题 @fanlintao """
    topics = Topic.objects.filter(creator=request.user).order_by("-last_reply_add")
    return render(request, "topics/created.html", {"topics": topics})


def replied_topic(request):
    """我回复的话题 @fanlintao """
    topics = Topic.objects.filter(id__in=Reply.objects.all().order_by('-create_time').filter(creator=request.user).values_list('topic', flat=True))
    return render(request, "topics/replied.html", {"topics": topics})


def topic_detail(request, topic_id):
    """ 话题详细页 @fanlintao """
    try:
        topic = Topic.objects.get(id=topic_id)
        replies = Reply.objects.filter(topic=topic).order_by("create_time")
        recent_topics = Topic.objects.filter(group=topic.group).order_by("-create_time")[:5]

        # 判断当前用户是否是该小组成员和管理员
        is_member, is_manager = request.user in topic.group.member.all(), request.user in topic.group.member.all()

        if request.method == "POST":
            form = replyForm(request.POST)
            print request.POST
            if form.is_valid():
                try:
                    reply = Reply.objects.get(id=request.POST.get('reply_id'))
                    print reply
                except:
                    reply = None
                print reply
                g = form.save(commit=False)
                g.creator = request.user
                g.topic = topic
                if reply:
                    g.reply = reply
                g.save()
        return render(request, "topics/detail.html", {"topic": topic, "replies": replies, "is_member": is_member,
                                                      "is_manager": is_manager, 'recent_topics': recent_topics,
                                                      'form': replyForm()})
    except ObjectDoesNotExist:
        pass