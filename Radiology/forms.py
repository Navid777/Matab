# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User


username_label = "نامِ کاربری"
password_label = "گذرواژه"

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'username'}), label=username_label)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'username'}), label=password_label)

    def __unicode__(self):
        return self.username

    def clean_username(self):
        username = self.cleaned_data['username']
        if not User.objects.filter(username=username):
            raise forms.ValidationError("No such user.")
        return username
    def clean_password(self):
        password = self.cleaned_data['password']
        if not password :
            raise forms.ValidationError("Enter a password.")
        return password
    def clean(self):
        cd = super(LoginForm, self).clean()
        username = cd.get('username')
        password = cd.get('password')
        user = authenticate(username=username,password= password)
        if user is not None:
            if user.is_active :
                pass
            else:
                raise forms.ValidationError('User is not active.')
        else:
            raise forms.ValidationError('Username/Password invalid.')

        return cd

