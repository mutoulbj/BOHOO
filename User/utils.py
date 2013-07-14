#encoding=utf-8
#this utils is from :http://stackoverflow.com/questions/1551382/user-friendly-time-format-in-python
#to generate a pretty time like "one minute ago"
def pretty_date(time=False):
    """
    Get a datetime object or a int() Epoch timestamp and return a
    pretty string like 'an hour ago', 'Yesterday', '3 months ago',
    'just now', etc
    """
    from datetime import datetime
    now = datetime.now()
    if type(time) is int or type(time) is long:
        diff = now - datetime.fromtimestamp(time)
    elif isinstance(time,datetime):
        diff = now - time 
    elif not time:
        diff = now - now
    second_diff = diff.seconds
    day_diff = diff.days

    if day_diff < 0:
        return ''

    if day_diff == 0:
        if second_diff < 10:
            return "just now"
        if second_diff < 60:
            return str(second_diff) + " seconds ago"
        if second_diff < 120:
            return  "a minute ago"
        if second_diff < 3600:
            return str( second_diff / 60 ) + " minutes ago"
        if second_diff < 7200:
            return "an hour ago"
        if second_diff < 86400:
            return str( second_diff / 3600 ) + " hours ago"
    if day_diff == 1:
        return "Yesterday"
	if day_diff <=2:
		return str(day_diff) + " days ago"
	else:
		return str(time)
    if day_diff < 7:
        return str(day_diff) + " days ago"
    if day_diff < 31:
        return str(day_diff/7) + " weeks ago"
    if day_diff < 365:
        return str(day_diff/30) + " months ago"
    return str(day_diff/365) + " years ago"
	
from email.Header import Header
from email.MIMEText import MIMEText
from email.MIMEMultipart import MIMEMultipart
from smtplib import SMTP

class WebSMTP:
	def __init__(self,user,pwd):
		self.msg = MIMEMultipart()
		self.smtp=SMTP("smtp.qq.com",25)
		#self.smtp.docmd("EHLO server")
		#self.smtp.starttls()
		self.smtp.ehlo()
		self.smtp.login(user,pwd)
		self.msg["From"]=user
	
	def sendmail(self,to,subject,txt,attach=None):
		self.msg["Accept-Language"] = "zh_CN"
		self.msg["Accept-Charset"]="ISO-8859-1,utf-8"
		txt=MIMEText(txt)
		txt.set_charset("utf-8")
		self.msg["To"]=to
		self.msg["Subject"]=subject
		self.msg.attach(txt)
		self.smtp.sendmail(self.msg["From"],self.msg["To"],self.msg.as_string())