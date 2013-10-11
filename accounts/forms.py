#! -*- coding:utf-8 -*-
from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate
from captcha.fields import CaptchaField    # django-simple-captcha  验证码字段
from User.models import MyUser


class login_form(forms.Form):
    """
    登录
    """
    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={
                'placeholder': u'邮件',
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': u'密码',
            }
        )
    )
    captcha = CaptchaField(error_messages={'invalid': u'验证码错误.'})

    def __init__(self, request=None, *args, **kwargs):
        """
        If request is passed in, the form will validate that cookies are
        enabled. Note that the request (a HttpRequest object) must have set a
        cookie with the key TEST_COOKIE_NAME and value TEST_COOKIE_VALUE before
        running this validation.
        """
        self.request = request
        self.user_cache = None
        super(login_form, self).__init__(*args, **kwargs)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            self.user_cache = authenticate(email=email, password=password)
            if self.user_cache is None:
                raise forms.ValidationError(u"邮箱或密码错误")
            elif not self.user_cache.is_active:
                raise forms.ValidationError(u"该帐号已被禁用")
        return self.cleaned_data

    def get_user_id(self):
        if self.user_cache:
            return self.user_cache.id
        return None

    def get_user(self):
        return self.user_cache


class register_form(forms.Form):
    """
    注册
    """
    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={
                'placeholder': u'邮件',
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': u'密码',
            }
        )
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': u'重复密码',
            }
        )
    )
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder': u'用户名',
            }
        )
    )

    def __init__(self, large_input=True, *args, **kwargs):
        super(register_form, self).__init__(*args, **kwargs)
        if large_input:
            self.fields['email'].widget.attrs.update({'class': 'input-xxlarge'})
            self.fields['password'].widget.attrs.update({'class': 'input-xxlarge'})
            self.fields['password1'].widget.attrs.update({'class': 'input-xxlarge'})
            self.fields['username'].widget.attrs.update({'class': 'input-xxlarge'})

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            MyUser.objects.get(email=email)
        except ObjectDoesNotExist:
            return email
        raise forms.ValidationError(u'该邮箱已经存在')

    def clean_password1(self):
        data = self.cleaned_data
        password = data['password']
        if len(password) < 6:
            raise forms.ValidationError(u'密码必须长于6字节')
        password1 = data['password1']
        if password == password1:
            return password1
        raise forms.ValidationError(u'密码必须一致')

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            MyUser.objects.get(username=username)
        except ObjectDoesNotExist:
            return username
        raise forms.ValidationError(u'该用户名已经存在')

    def save(self):
        data = self.cleaned_data
        MyUser.objects.create_user(email=data['email'], username=data['username'], password=data['password'])


class password_reset_apply_form(forms.Form):
    """  申请重置密码 """
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': u'邮件',}))
    captcha = CaptchaField(error_messages={'invalid': u'验证码错误.'})

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            try:
                user = MyUser.objects.get(email=email)
                return email
            except ObjectDoesNotExist:
                raise forms.ValidationError(u"该邮箱不存在!")

    def get_email(self):
        return self.cleaned_data['email']


class reset_password_form(forms.Form):
    """ 重置密码 """
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': u'新密码',}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': u'重复密码',}))
    captcha = CaptchaField(error_messages={'invalid': u'验证码错误.'})


    def clean_password1(self):
        data = self.cleaned_data
        password = data['password']
        if len(password) < 6:
            raise forms.ValidationError(u'密码必须长于6字节')
        password1 = data['password1']
        if password == password1:
            return password1
        raise forms.ValidationError(u'密码必须一致')
