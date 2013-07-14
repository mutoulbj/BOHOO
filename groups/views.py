# Create your views here.
#coding=utf-8
import random,hashlib
#from itertools import chain
import re
import os
import datetime
import time
import cStringIO
import urllib
from PIL import Image
import django
from django.http import HttpResponse,Http404
from django.shortcuts import render_to_response,redirect,render
from django.template import RequestContext

from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings

from django.db.models import F,Q
from models import Group_memeber,Catelog,Group,Topic,Topic_reply_amount,Reply,Report
import group_utils

SHA1_RE = re.compile('^[a-f0-9]{40}$')  

User = get_user_model()

SEARCH_GROUP = '9999'
SEARCH_TOPIC = '8888'

def home(request):
	vars = {}
	tag = request.GET.get("tag","")
	if tag == "":
		groups = Group.objects.all()[:20]
		vars["groups"] = groups
		d = group_utils.getCatelog()
		vars['catelog'] = d
		return render(request,'index.html',vars)
	else:
		catelog = Catelog.objects.get(cate_name=tag)
		#this means the catelog is a root catelog
		if catelog.parent_id == -1:
			#get all child catelog
			child_catelogs = Catelog.objects.filter(parent_id=catelog.id)
			all_groups = []
			for child_catelog in child_catelogs:
				group = Group.objects.filter(catelog=child_catelog)
				all_groups.extend(group)
			vars["groups"] = all_groups
			d = group_utils.getCatelog()
			vars['catelog'] = d
			vars['tag'] = tag
			return render(request,'index.html',vars)
		groups = Group.objects.filter(catelog=catelog)
		vars["groups"] = groups
		d = group_utils.getCatelog()
		vars['catelog'] = d
		vars['tag'] = tag
		return render(request,'index.html',vars)
		
def explore_topic(request):
	'''
		explore topics
		reply = [(topic,rep) for rep in [Topic_reply_amount.objects.filter(topic=topic)]]
	'''
	vars = {}
	tag = request.GET.get("tag","")
	if tag == "":
		topics = Topic.objects.all()[:20]
		topic_reply = []
		for topic in topics:
			reply = [(topic,rep) for rep in [Topic_reply_amount.objects.filter(topic=topic)]]
			topic_reply.append(reply)
		vars["topics"] = topic_reply
		d = group_utils.getCatelog()
		vars['catelog'] = d
		return render(request,'explore_topics.html',vars)
	else:
		catelog = Catelog.objects.get(cate_name=tag)
		if catelog.parent_id == -1:
			child_catelogs = Catelog.objects.filter(parent_id=catelog.id)
			all_groups = []
			for child_catelog in child_catelogs:
				group = Group.objects.filter(catelog=child_catelog)
				all_groups.extend(group)
			all_topics = []
			topic_reply = []
			if len(all_groups) > 0:
				for gp in all_groups:
					topics = Topic.objects.filter(group=gp)
					all_topics.extend(topics)
				for topic in all_topics:
					reply = [(topic,rep) for rep in [Topic_reply_amount.objects.filter(topic=topic)]]
					topic_reply.append(reply)
			vars["topics"] = topic_reply
			d = group_utils.getCatelog()
			vars['catelog'] = d
			vars["tag"] = tag
			return render(request,'explore_topics.html',vars)
		else:
			group = Group.objects.filter(catelog=catelog)
			topic_reply = []
			all_topics = []
			if group.count() > 0:
				for gp in group:
					topics = Topic.objects.filter(group=gp)
					all_topics.extend(topics)
				for topic in all_topics:
					reply = [(topic,rep) for rep in [Topic_reply_amount.objects.filter(topic=topic)]]
					topic_reply.append(reply)
			vars["topics"] = topic_reply
			d = group_utils.getCatelog()
			vars['catelog'] = d
			vars["tag"] = tag
			return render(request,'explore_topics.html',vars)
	
def register(request):
	vars = {}
	if request.method == "POST":
		form_email = request.POST.get("form_email",'')
		form_password = request.POST.get("form_password",'')
		form_name = request.POST.get("form_name",'')
		captcha = request.POST.get('captcha-solution','')
		if form_email == "" or form_password == '' or form_name == '':
			vars['msg'] = 'empty error!'
			return render(request,'join.html',vars)
		if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", form_email) == None:
			vars['msg'] = 'email 不合法!'
			return render(request,'join.html',vars)
		if captcha == '':
			vars['msg'] = 'captcha empty error!'
			return render(request,'join.html',vars)
		if captcha.lower() != request.session.get("captcha_code",""):
			vars['msg'] = 'captcha  error!'
			return render(request,'join.html',vars)
		user_indb = User.objects.filter(email=form_email).count()
		#if len(user_indb) > 0:
		if user_indb > 0:
			vars['msg'] = 'user exists!'
			return render(request,'join.html',vars)
		nickname_indb = User.objects.filter(nickname=form_name).count()
		if nickname_indb > 0:
			vars['msg'] = 'nickname exists!'
			return render(request,'join.html',vars)
		user = User.objects.create_user(email=form_email, nickname=form_name, password=form_password)
		
		salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
		username = user.email  
		if isinstance(username, unicode):  
			username = username.encode('utf-8')  
		activation_key = hashlib.sha1(salt+username).hexdigest()  
		user.activation_key=activation_key
		user.is_active=0
		user.save()
		user_auth = authenticate(username=form_email,password=form_password)
		django.contrib.auth.login(request,user_auth)
		try:
			user.send_activation_email(username,'group') 
		except Exception:
			return HttpResponse("发信失败，请重试或者联系管理员：xxx@ddd.com")
			
		return redirect('/accounts/wait_activate')
	return render_to_response('join.html', context_instance=RequestContext(request))
	
def get_captcha(request):
	c=group_utils.picChecker() 
	t=c.createChecker()
	request.session["captcha_code"] = t[0].lower()
	buf = cStringIO.StringIO()
	t[1].save(buf,'gif')
	return HttpResponse(buf.getvalue(),'image/gif')
	#print(t)
	
	
def login(request):
	vars = {}
	if request.method == 'POST':
		form_email = request.POST.get("form_email",'')
		form_password = request.POST.get("form_password",'')
		if form_email == '' or form_password == '':
			vars['msg'] = 'empty error'
			return render(request,'login.html',vars)
		#return HttpResponse(str([form_email,form_password]))
		if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", form_email) == None:
			vars['msg'] = 'email不合法'
			return render(request,'login.html',vars)
		user = authenticate(username=form_email,password=form_password)

		if user is not None:
			user_activate = user.is_active
			if user_activate == 0:
				return redirect('/accounts/wait_activate')
			django.contrib.auth.login(request,user)
			member = Group_memeber.objects.filter(member=user)
			next =request.META['HTTP_REFERER']
			#print 'next:',next
			#next is like http://localhost:8000/group/login?next=/group/name
			if "?" in next:
				
				next = next.split("?")[-1].split("=")[-1]
				keys = urllib.unquote_plus(next.split("/")[-2])
				if keys == "mygroup":
					#return redirect mygroup page
					return redirect("mygroup")
				group_name = urllib.unquote_plus(keys)

				try:
					group_db = Group.objects.get(name=group_name)
				except ObjectDoesNotExist:
					raise Http404()
				if request.user not in group_db.member.all():
					group_db.member.add(request.user)
				return redirect(next)
			#user has not join any group yet!
			if len(member) == 0 :
				d = group_utils.getCatelogAndGroup()
				vars['catelog'] = d
				return render(request,'guide.html',vars)
				#return redirect('guide')
			return redirect("mygroup")
			
		else:
			vars['msg'] = 'username or password incorrect'
			return render(request,'login.html',vars)
			#return HttpResponse("login failed!")
	return render(request,"login.html")

@login_required	
def groupjoin(request):
	user = request.POST.get("user",'')
	group = request.POST.get("group",'')
	if user != '' and group != '':
		#return HttpResponse(str([user,group]))
		group_db = Group.objects.filter(name=group)
		if request.user in group_db[0].member.all():
			#-1 means user already join the group
			return HttpResponse("-1")
		if len(group_db) != 0:
			group_db[0].member.add(request.user)
			return HttpResponse("0")
	return HttpResponse("-2")
	

	
def logout(request):
	django.contrib.auth.logout(request)
	return redirect("home")
	
#@login_required
def guide(request):
	vars = {}
	d = group_utils.getCatelogAndGroup()
	print "d is:",d
	vars['catelog'] = d
	return render(request,'guide.html',vars)

@login_required	
def mygroup(request):
	'''
		show topics in my group
	'''
	vars = {}
	vars["tp"] = "all"
	mygroups = Group.objects.filter(member=request.user)
	#print "mygroup is:",mygroups
	d = []
	#now = datetime.datetime.now()
	#month_one = datetime.datetime(now.year,now.month,1)
	topics = []
	for group in mygroups:
		#topics = [topic for topic in Topic.objects.filter(group=group).order_by("-last_reply_add")[:500]]
		tps = Topic.objects.filter(group=group).order_by("-last_reply_add")
		topics.append(tps)
	#print "topics:",topics
	if len(topics) > 0:
		for topic in topics:
			if len(topic)>0:
					for t in topic:
						d.append([(t,rep) for rep in [Topic_reply_amount.objects.filter(topic=t)]])
					#reply = [(t,rep) for rep in [Topic_reply_amount.objects.filter(topic=t) for t in topic ]]
					#d.append(reply)

	vars["mygroups"] = d
	return render(request,'mygroup.html',vars)

@login_required	
def my_topics(request):
	'''
		display the topics published by the current login user
	'''
	vars = {}
	vars["tp"] = "me"
	mygroups = Group.objects.filter(member=request.user)
	d = []
	topics = []
	for group in mygroups:
		#topics = [topic for topic in Topic.objects.filter(group=group,creator=request.user).order_by("-last_reply_add")]
		tps = Topic.objects.filter(group=group,creator=request.user).order_by("-last_reply_add")
		topics.append(tps)

	if len(topics) > 0:
		for topic in topics:
			if len(topic)>0:
				for t in topic:
					d.append([(t,rep) for rep in [Topic_reply_amount.objects.filter(topic=t)]])
				#reply = [(topic,rep) for rep in [Topic_reply_amount.objects.filter(topic=topic)]]
				#d.append(reply)
	vars["mygroups"] = d
	return render(request,'mygroup.html',vars)
	
@login_required
def my_replied_topics(request):
	'''
		display the topics that current user response
	'''
	vars = {}
	vars["tp"] = "res"
	d = []
	
	replys = Reply.objects.filter(creator=request.user)
	topic_set = set()
	for rep in replys:
		topic_set.add(rep.topic)
	temp_list = []
	for ts in topic_set:
		if Reply.objects.filter(topic=ts).count() > 0:
			temp_list.append(Reply.objects.filter(topic=ts)[0])
 
	for reply in temp_list:
		tp = [(reply.topic,rep) for rep in [Topic_reply_amount.objects.filter(topic=reply.topic)]]
		d.append(tp)
	vars["mygroups"] = d
	return render(request,'mygroup.html',vars)

@login_required
def mine(request):
	'''
		show the group user join or created
	'''
	adminGroup = None
	joinGroups = None
	vars = {}
	adminGroups = Group.objects.filter(creator=request.user)
	joinGroups = Group.objects.filter(member=request.user)
	vars['adminGroups'] = adminGroups
	vars['joinGroups']  = joinGroups
	return render(request,'mine.html',vars)
	
#func to view topic
def topic(request,id):
	vars = {}
	
	topic = Topic.objects.filter(id=id)
	voteid = request.COOKIES.get('vote','')
	vars["voteid"] = voteid
	
	action = request.GET.get("action","")
	if request.method == "POST":
		if action == "edit":
			rev_title = request.POST.get("rev_title","")
			rev_text  = request.POST.get("rev_text","")
			image_names = request.POST.get("image_names","")
			images =  image_names.split("|")[:-1]
			image_str = ""
			for im in images:
				image_str += "%s<br/>"%im
			rev_text = image_str+">>>>||>>>>"+rev_text
			if rev_title != "" and rev_text != "":
				topic.update(name=rev_title,content=rev_text)
				return redirect("topic",id=id)
	if action != "":
		if request.user.is_authenticated():
			if request.user == topic[0].creator:
				if action == "sticky":
					topic.update(is_top=1)
					return redirect("topic",id=id)
				elif action == "unsticky":
					topic.update(is_top=0)
					return redirect("topic",id=id)
				elif action == "edit":
					vars["topic"] = topic
					return render(request,'edit_topic.html',vars)
			
			if action == "ding":
				if voteid != id:
					topic = Topic.objects.get(pk=id)
					topic.ilike = F('ilike') + 1
					topic.save()
					response = redirect("topic",id=id)
					response.set_cookie('vote', id)
					return response
			elif action == "cai":
				if voteid != id:
					topic = Topic.objects.get(pk=id)
					topic.dislike = F('dislike') + 1
					topic.save()
					response = redirect("topic",id=id)
					response.set_cookie('vote', id)
					return response
	five_new_topic = Topic.objects.filter(group=topic[0].group)
	if len(five_new_topic) > 5:
		five_new_topic = five_new_topic[:5]
	author = request.GET.get("author","")
	if author != "":
		author_user = User.objects.get(nickname=author)
		reply = Reply.objects.filter(topic=topic,creator=author_user)
	else:
		reply = Reply.objects.filter(topic=topic)
	vars["topic"] = topic
	vars["reply"] = reply
	vars["new_topic"] = five_new_topic
	
	return render(request,'topic_view.html',vars)
	
def remove_comment(request,id):
	'''
		remove a comment
	'''
	if request.is_ajax():
		if not request.user.is_authenticated():
			return HttpResponse(-1)
		cid = request.POST.get("cid","")
		if cid != "":
			Reply.objects.filter(id=cid).delete()
			return HttpResponse(0)
		return HttpResponse(-2)
	return HttpResponse("")
	
def admin_remove(request,id):
	'''
		remove a topic
	'''
	if request.user.is_authenticated():
		topic = Topic.objects.get(pk=id)
		if request.user == topic.group.creator:
			topic.delete()
			return redirect("showgroup",gname=topic.group.name)
	return HttpResponse("")
		
	
def add_comment(request,tid):
	'''
		func add comment
	'''
	content = request.POST.get("rv_comment",'')
	if content.strip() == '':
		return redirect("topic",id=tid)
	ref_user = request.POST.get("ref_user","")
	ref_content = request.POST.get("ref_content","")
	all_content = content
	if ref_user != '' and ref_content != '':
		all_content = "||"+ref_content+"    "+ref_user+"""  \n\n
			%s
		"""%content
	topic = Topic.objects.get(id=tid)
	reply = Reply(content=all_content,creator=request.user,topic=topic)
	reply.save()
	#we need to update the Topic_reply_amount table
	topic_reply_amount = Topic_reply_amount.objects.get(topic=topic)
	topic_reply_amount.amount  = F('amount') + 1
	topic_reply_amount.save()
	return redirect("topic",id=tid)
	

#@login_required
def showgroup(request,gname,template='show_group.html'):
	'''
		func to join a group then redirect the previous topic page
	'''
	vars = {}
	action = request.GET.get('action','')
	group = Group.objects.get(name=gname)
	#user join group
	if action == "join":
		if not request.user.is_authenticated():
			#deal to the args we can not user url name directly
			return redirect('/group/login?next=%s' % request.path)
		try:
			if request.user not  in group.member.all():
				group.member.add(request.user)
			return redirect("showgroup",gname=gname)
		except ObjectDoesNotExist:
			raise Http404()
	#user quit group
	elif action == "quit":
		#we also need to check user
		if request.user.is_authenticated():
			if request.user in group.member.all():
				group.member.remove(request.user)
				return redirect('showgroup',gname=gname)
	#to view a group by it's name ,so the group name is unique
	#we should be check whether the group is exists when user create a group.
	
		
	topics = Topic.objects.filter(group=group)
	d = []
	for topic in topics:
		topic_reply = [(topic,rep) for rep in [Topic_reply_amount.objects.filter(topic=topic)]]
		d.append(topic_reply)
		
	tp = request.GET.get("type","")
	if tp != "":
		if tp == "essence":
			vars["tp"] = tp
			new_d = sorted(d,key=lambda s:s[0][1][0].amount,reverse=True)
			vars["topics"] = new_d
			vars["group"] = group
			return render(request,template,vars)
	vars["topics"] = d
	vars["group"] = group
	return render(request,template,vars)
	
#func to search groups or topics
def search(request):
	q = request.GET.get('q','')
	cat = request.GET.get('cat','')
	group_name = request.GET.get("group","")
	if q.strip() == '' or cat == '':
		return redirect("/group")
	else:
		vars = {}
		vars["q"] = q
		vars['cat'] = cat
		print cat == SEARCH_GROUP
		if cat == SEARCH_GROUP:
			groups = Group.objects.filter(name__icontains='%s'%q)
			vars['groups'] = groups
		elif cat == SEARCH_TOPIC:
			#get name or content 
			if group_name != "":
				current_group_object = Group.objects.get(name=group_name)
				vars["current_group"] = group_name
				topics = Topic.objects.filter(group=current_group_object).filter(Q(name__icontains='%s'%q) | Q(content__icontains='%s'%q))
			else:
				topics = Topic.objects.filter(Q(name__icontains='%s'%q) | Q(content__icontains='%s'%q))
			d = []
			for topic in topics:
				topic_reply = [(topic,rep) for rep in [Topic_reply_amount.objects.filter(topic=topic)]]
				d.append(topic_reply)
			vars["topics"] = d
			
		
		return render(request,'search_rs.html',vars)
	
#func : to create a new group
def new_group(request):
	#use must be login
	if not request.user.is_authenticated():
		return redirect("/group")
	vars = {}
	if request.method == 'POST':
		ck = request.POST.get("ck","")
		#we need to get another page for create group form
		if ck == 'first':
			#get group catelog parent_id = -1 (we defined)
			#cats = Catelog.objects.filter(parent_id =-1)
			cats = Catelog.objects.filter(~Q(parent_id = -1) & ~Q(parent_id = -2))
			#cats = Catelog.objects.filter(~Q(parent_id = -2))
			vars["cats"] = cats
			return render(request,'new_group2.html',vars)
		elif ck == 'second':
			site_type = request.POST.get("site_type","")
			grp_name  = request.POST.get("grp_name","")
			grp_content = request.POST.get("grp_content","")
			tags      = request.POST.get("tags","")
			if site_type == '' or grp_name == '' or grp_content == '' or tags == '':
				vars["msg"] = "empty error"
				return render(request,'new_group2.html',vars)
			group_indb = Group.objects.filter(name=grp_name).count()
			if group_indb > 0 :
				vars["msg"] = "group already exists! please use another name"
				return render(request,'new_group2.html',vars)
			cate = Catelog.objects.get(cate_name=tags)
			group = Group(name=grp_name,description=grp_content,catelog=cate,creator=request.user,type=site_type)
			group.save()
			group.member.add(request.user)
			return redirect("showgroup",gname=grp_name)
		return redirect("/group")
		#create group begin
		
	return render(request,'new_group.html',vars)

@login_required	
def new_topic(request,gname):
	'''
		login user add a new topic
	'''
	vars = {}
	group = Group.objects.get(name=gname)
	vars['group'] = group
	if request.method == "POST":
		rev_title = request.POST.get("rev_title","")
		rev_text  = request.POST.get("rev_text","")
		image_names = request.POST.get("image_names","")
		if rev_text == "" or rev_title == '':
			vars["msg"] = "标题和内容不能不写啊"
			return render(request,'new_topic.html',vars)
		images =  image_names.split("|")[:-1]
		image_str = ""
		for im in images:
			image_str += "%s<br/>"%im
		rev_text = image_str+">>>>||>>>>"+rev_text
		topic = Topic(name=rev_title,content=rev_text,group=group,creator=request.user)
		topic.save()
		topic_amount = Topic_reply_amount(topic=topic,amount=0)
		topic_amount.save()
		return redirect("topic",id=topic.id)
	return render(request,'new_topic.html',vars)
	
@login_required
def group_edit(request,gname):
	'''
		for group admin managememt
	'''
	vars = {}
	group = Group.objects.get(name=gname)
	
	vars["group"] = group
	cats = Catelog.objects.filter(~Q(parent_id = -1) & ~Q(parent_id = -2))
	vars["cats"] = cats
	if request.method == "POST":
		grp_name = request.POST.get("grp_name","")
		grp_intro = request.POST.get("grp_intro","")
		tags = request.POST.get("tags","")
		grp_role_mbr = request.POST.get("grp_role_mbr","")
		grp_role_adm = request.POST.get("grp_role_adm","")
		file = request.FILES.get("file","")

		#check if anything to update
		if grp_name == group.name and grp_intro == group.description and tags == group.catelog.cate_name and grp_role_mbr == group.member_nick:
			if file == "":
				return redirect('showgroup',gname=grp_name)
			else:
				#filecontent = file.read()
				group.image.save(request.FILES['file'].name,request.FILES['file'])
				return redirect('showgroup',gname=grp_name)
		#check null
		if grp_name == '' or grp_intro == '' or tags == '' or grp_role_mbr == '' or grp_role_adm == '':
			vars["msg"] = "empty error,check input"
			return render(request,'group_edit.html',vars)
		if grp_name != group.name:
			group_indb = Group.objects.filter(name=grp_name).count()
			if group_indb > 0 :
				vars["msg"] = "group name is already in use!"
				return render(request,'group_edit.html',vars)
		#update group info
		cate = Catelog.objects.get(cate_name=tags)
		
		Group.objects.filter(name=gname).update(name=grp_name,description=grp_intro,catelog=cate,member_nick=grp_role_mbr,modify_time=datetime.datetime.now())
		return redirect('showgroup',gname=grp_name)
	
	return render(request,'group_edit.html',vars)
	
@login_required
def members(request,gname):
	'''
		group admin show member info 
	'''
	vars = {}
	group = Group.objects.get(name=gname)
	vars["group"] = group
	return render(request,'members.html',vars)
	
@login_required
def advance(request,gname):
	'''
		group advance manage
	'''
	vars = {}
	group = Group.objects.get(name=gname)
	vars['group'] = group
	return render(request,'advance.html',vars)
	
def add_friendgroup(request):
	'''
		add a friend group
	'''
	if not request.user.is_authenticated():
		return HttpResponse(-1)
	if request.method == "POST":
		groupname = request.POST.get("name","")
		current_group = request.POST.get("current_group","")
		#check group input exists
		try:
			group = Group.objects.get(name=groupname)
		except ObjectDoesNotExist:
			#group not exist
			return HttpResponse(-3)
		user_group = Group.objects.get(name=current_group)
		user_group.gfriend.add(group)
		return HttpResponse(0)
		
def change_privacy(request):
	'''
		group privacy change 
	'''
	if not request.user.is_authenticated():
		return HttpResponse(-1)
	if request.method == "POST":
		current_group = request.POST.get("current_group","")
		privacy = request.POST.get("privacy","")
		user_group = Group.objects.get(name=current_group)
		user_group.type=int(privacy)
		user_group.save()
		return HttpResponse(0)
	
def change_join(request):
	'''
		change group's join type
	'''
	if not request.user.is_authenticated():
		return HttpResponse(-1)
	if request.method == "POST":
		current_group = request.POST.get("current_group","")
		join_type = request.POST.get("join_type","")
		user_group = Group.objects.get(name=current_group)
		user_group.member_join=int(join_type)
		user_group.save()
		return HttpResponse(0)
		
def user_report(request):
	'''
		report handle
	'''
	if request.method == "POST":
		rep_id = request.POST.get("rep_id","")
		rep_type = request.POST.get("rep_type","")
		reason   = request.POST.get("reason","")
		if rep_id == '' or rep_type == '' or reason == '':
			return HttpResponse(-3)
		report = Report(rep_type=int(rep_type),beReported=rep_id,reason=reason)
		report.save()
		return HttpResponse(0)
		

		
def upload_images(request):
	"""
		create topic upload image
	"""
	if not request.user.is_authenticated():
		return HttpResponse(-1)
	fs =  request.FILES.get('Filedata',None)
	if fs == None:
		return HttpResponse(-2)
	allow_type = ["jpg","png","gif","jpeg"]
	if fs.name.split(".")[-1] not in allow_type:
		return HttpResponse(-3)
	filename = time.strftime("%Y%M%d%M%H%S", time.localtime())+"."+fs.name.split(".")[-1]
	im = Image.open(fs.file)
	width,height = im.size
	if width > 500 or height > 500:
		width,height = width/2,height/2
	im = im.resize((width,height),Image.ANTIALIAS)
	quality_val = 90
	im.save(settings.MEDIA_ROOT+"/upload/"+filename, 'JPEG', quality=quality_val)
	
	#f = open(settings.MEDIA_ROOT+"/upload/"+filename,"wb")
	#f.write(fs.file.getvalue())
	#f.close()
	return HttpResponse(filename)
	
def del_image(request):
	"""
		delete an upload image
		
	"""
	if not request.user.is_authenticated():
		return HttpResponse(-1)
	img_name = request.POST.get("img_name","")
	if img_name == "":
		return HttpResponse(-2)
	file = settings.MEDIA_ROOT+"/upload/"+img_name
	if os.path.exists(file):
		os.remove(file)
		return HttpResponse(0)
	return HttpResponse(-3)
	
	
def activate(request, activation_key):  
    if SHA1_RE.search(activation_key):  
		try:  
			user = User.objects.get(activation_key=activation_key)
		except :  
			return render_to_response('error.html', RequestContext(request, locals()))  
		if not user.activation_key_expired():  
			user.is_active = 1  
			user.save()  
			user.activation_key = u"ALREADY_ACTIVATED"  
			user.save()
			return render_to_response('activate_complete.html', RequestContext(request, locals()))

def wait_activate(request):  
    return render_to_response('wait_activate.html', RequestContext(request, locals())) 			
	
	
def dispatcher(request,page):
	if page == 'blank':
		return render_to_response('blank.htm')
