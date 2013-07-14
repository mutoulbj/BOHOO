#coding=utf-8
import datetime
from django import template
from django.utils import timezone
register = template.Library()

@register.filter
def timeformat(date):
	if type(date) is float:
		date = datetime.datetime.fromtimestamp(date)
	#end = datetime.datetime.now()
	end = timezone.now()
	delta = end - date
	days = delta.days
	seconds = delta.seconds
	#if days > 365:
	#	years = int(days / 365)
	#	return "%d年前" % years
	#if days > 30:
	#	months = int(days / 30)
	#	return "%d个月前" % months
	#if days > 7:
	#	weeks = int(days / 7)
	#	return "%d周前" % weeks
	if days >=2:
		return date
	if days > 0:
		return "%d天前" % days
	if seconds > 3600:
		hours = int(seconds / 3600)
		return "%d个小时前" % hours
	if seconds > 60:
		minutes = int(seconds / 60)
		return "%d分钟前" % minutes
	return "1分钟前"