# Create your views here.
#coding=utf-8
import json
import datetime
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.utils.datastructures import MultiValueDictKeyError
from groups.models import Group, Topic, Reply, Applicant, TopicImage, Report
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from User.models import MyUser
from groups.forms import group, topicForm, replyForm, topicImageForm
from groups.models import Category
from groups.utils import get_most_topic_groups
from sys_notification.signals import group_notify, topic_notify


def new_group(request):
    """ 创建群组 @fanlintao """
    if request.method == 'POST':
        form = group(request.POST)
        if form.is_valid():
            g = form.save(commit=False)
            g.creator = request.user
            g.category = Category.objects.get(name=request.POST['category'])  # 必须保证分类存在
            g.save()
            g.manager.add(request.user)   # 创建者默认是管理员
            g.member.add(request.user)    # 创建者默认是小组成员
            return redirect(reverse("add_group_avatar", kwargs={'group_id': g.id}))
            #return redirect(reverse("group_detail", args=[g.id]))
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
                g.category = Category.objects.get(name=request.POST['category'])  # 必须保证分类存在
                g.save()
                return redirect(reverse("group_my_manage"))
        return render(request, 'groups/edit.html', {'t_group': t_group, 'form': group(instance=t_group)})
    except ObjectDoesNotExist:
        pass


def add_group_avatar(request, group_id):
    """ 添加小组头像 """
    t_group = get_object_or_404(Group, id=group_id)
    return render(request, 'groups/new/add_avatar.html', {'group': t_group})


def group_detail(request, group_id):
    """ 群组详细页 @fanlintao"""
    try:
        group = Group.objects.get(id=group_id)
        is_member, is_manager, is_creator = False, False, False
        # 判断当前用户是不是小组成员
        if request.user in group.member.all():
            is_member = True
        # 判断当前用户是不是小组管理员
        if request.user in group.manager.all():
            is_manager = True
        # 判断当前用户是不是小组创建者
        if request.user == group.creator:
            is_creator = True
        # 判断当前用户申请加入该小组的请求是否正在处理中,若正在处理中,不允许重复申请
        try:
            if not request.user.is_anonymous():
                apply_is_processing = Applicant.objects.get(applicant=request.user, group=group, status="processing",
                                                            join_type="member")
                is_member_processing = True
            else:
                is_member_processing = False
        except ObjectDoesNotExist:
            is_member_processing = False

        try:
            if not request.user.is_anonymous():
                apply_is_processing = Applicant.objects.get(applicant=request.user, group=group, status="processing",
                                                            join_type="manager")
                is_manager_processing = True
            else:
                is_manager_processing = False
        except ObjectDoesNotExist:
            is_manager_processing = False

        topic_qs = Topic.objects.filter(group=group, status='enabled')
        topics_list = topic_qs.order_by("-last_reply_add")  # 默认按最近回复时间排序
        try:
            if request.GET['type'] == 'recent':   # 最近话题:按最近回复时间排序
                #topics_list = topic_qs.order_by("-last_reply_add")
                pass
            elif request.GET['type'] == 'hot':    # 最热话题:按回复数量排序
                topics_list = topic_qs.order_by("-reply_amount")
        except MultiValueDictKeyError:
            pass

        # 对话题分页
        paginator = Paginator(topics_list, settings.TOPIC_PAGINTION_PER_PAGE)
        page = request.GET.get('page')
        try:
            topics = paginator.page(page)
        except PageNotAnInteger:
            topics = paginator.page(1)
        except EmptyPage:
            topics = paginator.page(paginator.num_pages)

        if not request.user.is_anonymous():
            recommend_groups = get_most_topic_groups(request.user, 5)
        else:
            recommend_groups = None
        ctx = {
            'g': group, 'is_member': is_member, 'topics': topics,
            'is_creator': is_creator,
            'is_member_processing': is_member_processing,
            'is_manager': is_manager,
            'is_manager_processing': is_manager_processing,
            'recommend_groups': recommend_groups
        }
        return render(request, 'groups/detail.html', ctx)
    except ObjectDoesNotExist:
        pass


@login_required()
def ajax_join_group(request):
    """ 加入群组  ajax @fanlintao """
    error = {"success": "", "error": ""}
    if request.method == 'POST':
        group = Group.objects.get(id=request.POST.get("group_id"))
        group.member.add(request.user)
        error["success"] = "success"
        return HttpResponse(json.dumps(error, ensure_ascii=False), mimetype="application/json")


@login_required()
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
    """ 申请成为管理员 ajax @fanlintao """
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


@login_required()
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


@login_required()
def manage(request):
    """ 我管理的群组 @fanlintao """
    groups_list = Group.objects.filter(manager=request.user)
    # 对群组分页
    paginator = Paginator(groups_list, settings.GROUP_MANAGED_PER_PAGE)
    page = request.GET.get('page')
    try:
        groups = paginator.page(page)
    except PageNotAnInteger:
        groups = paginator.page(1)
    except EmptyPage:
        groups = paginator.page(paginator.num_pages)
    return render(request, 'groups/managed.html', {'groups': groups})


@login_required()
def joined(request):
    """  我加入的群组 @fanlintao """
    groups_list = Group.objects.filter(member=request.user)
    # 对群组分页
    paginator = Paginator(groups_list, settings.GROUP_JOINED_PER_PAGE)
    page = request.GET.get('page')
    try:
        groups = paginator.page(page)
    except PageNotAnInteger:
        groups = paginator.page(1)
    except EmptyPage:
        groups = paginator.page(paginator.num_pages)
    return render(request, 'groups/joined.html', {'groups': groups})


@login_required()
def apply_deal(request, group_id):
    """ 处理请求 @fanlintao """
    try:
        group = Group.objects.get(id=group_id)
        m_applicant = Applicant.objects.filter(group=group, status="processing", join_type="member")
        g_applicant = Applicant.objects.filter(group=group, status="processing", join_type="manager")
        return render(request, 'groups/apply_deal.html', {'m_applicant': m_applicant, 'g_applicant': g_applicant})
    except ObjectDoesNotExist:
        pass


@login_required()
def ajax_apply_pass(request):
    """ ajax 通过请求 @fanlintao """
    error = {"success": "", "error": ""}
    if request.method == 'POST':
        try:
            pass_type = request.POST.get("type")
            group = Group.objects.get(id=request.POST.get("group_id"))
            user = MyUser.objects.get(id=request.POST.get("applicant_id"))
            applicant = Applicant.objects.get(applicant=user, group=group, status="processing")
            if pass_type == "member":
                group.member.add(user)
            elif pass_type == "manager":
                group.manager.add(user)
            applicant.status = 'pass'
            applicant.save()
            group_notify.send(sender=applicant, instance=applicant)   # 发送signal
            error['success'] = 'success'
            return HttpResponse(json.dumps(error, ensure_ascii=False), mimetype="application/json")
        except ObjectDoesNotExist:
            error['error'] = 'error'
            return HttpResponse(json.dumps(error, ensure_ascii=False), mimetype="application/json")


@login_required()
def ajax_apply_reject(request):
    """ ajax 拒绝请求 @fanlintao """
    error = {"success": "", "error": ""}
    if request.method == 'POST':
        try:
            applicant = Applicant.objects.get(id=request.POST.get("applicant_id"), status="processing")
            applicant.status = 'reject'
            applicant.save()
            group_notify.send(sender=applicant, instance=applicant)   # 发送signal
            error['success'] = 'success'
            return HttpResponse(json.dumps(error, ensure_ascii=False), mimetype="application/json")
        except ObjectDoesNotExist:
            error['error'] = 'error'
            return HttpResponse(json.dumps(error, ensure_ascii=False), mimetype="application/json")


image_obj = []
@login_required()
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
            if form.is_valid():
                g = form.save(commit=False)
                g.creator = request.user
                g.save()
                if len(image_obj):
                    for i in image_obj:
                        g.image.add(i)
                image_obj = []
                g_id = int(group.id)
                return redirect(reverse("group_detail", kwargs={'group_id': g_id}) + '?type=recent')
        ctx = {
            'form': topicForm(initial={"group": group}),
            'g': group,
            'imageForm': topicImageForm(),
            'images': image_obj
        }
        return render(request, 'topics/new/topic.html', ctx)
    except ObjectDoesNotExist:
        pass


@login_required()
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
                return redirect(reverse("group_detail", kwargs={'group_id': g_id}) + '?type=recent')
        ctx = {
            'form': topicForm(instance=t_topic),
            'g': group,
            'imageForm': topicImageForm(),
            'images': image_obj
        }
        return render(request, 'topics/new/topic.html', ctx)
    except ObjectDoesNotExist:
        pass


@login_required()
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


@login_required()
def group_topic(request):
    """ 我的群组的话题 @fanlintao """
    groups = Group.objects.filter(member=request.user)
    topics_list = Topic.objects.filter(group__in=groups, status='enabled').order_by("-last_reply_add")[0: 100] # 显示100个
    paginator = Paginator(topics_list, settings.TOPIC_MYGROUP_PER_PAGE)
    page = request.GET.get('page')
    try:
        topics = paginator.page(page)
    except PageNotAnInteger:
        topics = paginator.page(1)
    except EmptyPage:
        topics = paginator.page(paginator.num_pages)
    return render(request, "topics/group.html", {"topics": topics})


@login_required()
def created_topic(request):
    """我创建的话题 @fanlintao """
    topics_list = Topic.objects.filter(creator=request.user, status='enabled').order_by("-last_reply_add")[0:100] # 显示100个
    paginator = Paginator(topics_list, settings.TOPIC_ADD_PER_PAGE)
    page = request.GET.get('page')
    try:
        topics = paginator.page(page)
    except PageNotAnInteger:
        topics = paginator.page(1)
    except EmptyPage:
        topics = paginator.page(paginator.num_pages)
    return render(request, "topics/created.html", {"topics": topics})


@login_required()
def replied_topic(request):
    """我回复的话题 @fanlintao """
    reply_ids = Reply.objects.all().order_by('-create_time').filter(creator=request.user).values_list('topic', flat=True)
    topics_list = Topic.objects.filter(id__in=reply_ids, status='enabled')[0:100]  # 显示100个
    paginator = Paginator(topics_list, settings.TOPIC_REPLY_PER_PAGE)
    page = request.GET.get('page')
    try:
        topics = paginator.page(page)
    except PageNotAnInteger:
        topics = paginator.page(1)
    except EmptyPage:
        topics = paginator.page(paginator.num_pages)
    return render(request, "topics/replied.html", {"topics": topics})


def topic_detail(request, topic_id):
    """ 话题详细页 @fanlintao """
    try:
        topic = Topic.objects.get(id=topic_id)
        recent_topics = Topic.objects.filter(group=topic.group, status='enabled').order_by("-create_time")[:5]
        replies_list = Reply.objects.filter(topic=topic, status='enabled').order_by("create_time")
        # 对回复分页
        paginator = Paginator(replies_list, settings.PAGINATION_PER_PAGE)
        page = request.GET.get('page')
        try:
            replies = paginator.page(page)
        except PageNotAnInteger:
            replies = paginator.page(1)
        except EmptyPage:
            replies = paginator.page(paginator.num_pages)

        # 判断当前用户是否是该小组成员和管理员
        is_member, is_manager = request.user in topic.group.member.all(), request.user in topic.group.member.all()

        if request.method == "POST":
            form = replyForm(request.POST)
            if form.is_valid():
                try:
                    reply = Reply.objects.get(id=request.POST.get('reply_id'))
                except ObjectDoesNotExist:
                    reply = None
                except ValueError:
                    reply = None
                g = form.save(commit=False)
                g.creator = request.user
                g.topic = topic
                if reply:
                    g.reply = reply
                g.save()
                topic_notify.send(sender=g, instance=g)
                return redirect(reverse('topic_detail', args=[topic_id]))
        topic.click_amount += 1
        topic.save()
        return render(request, "topics/detail.html", {"topic": topic, "replies": replies, "is_member": is_member,
                                                      "is_manager": is_manager, 'recent_topics': recent_topics,
                                                      'form': replyForm()})
    except ObjectDoesNotExist:
        pass


def ajax_report_topic(request):
    error = {'error': '', 'success': ''}
    if request.method == 'POST':
        try:
            topic = Topic.objects.get(id=request.POST['topic_id'])
            reason = request.POST['reason']
            report = Report(report_type='topic', topic=topic, user=request.user, reason=reason)
            report.save()
            error['success'] = 'success'
            return HttpResponse(json.dumps(error, ensure_ascii=False), mimetype="application/json")
        except ObjectDoesNotExist:
            error['error'] = 'error'
            return HttpResponse(json.dumps(error, ensure_ascii=False), mimetype="application/json")


def ajax_report_reply(request):
    error = {'error': '', 'success': ''}
    if request.method == 'POST':
        try:
            reply = Reply.objects.get(id=request.POST['reply_id'])
            reason = request.POST['reason']
            report = Report(report_type='reply', reply=reply, user=request.user, reason=reason)
            report.save()
            error['success'] = 'success'
            return HttpResponse(json.dumps(error, ensure_ascii=False), mimetype="application/json")
        except ObjectDoesNotExist:
            error['error'] = 'error'
            return HttpResponse(json.dumps(error, ensure_ascii=False), mimetype="application/json")
