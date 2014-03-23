# -*- coding: utf-8 -*-
import datetime
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from Radiology.forms import LoginForm
from django.contrib.auth import login, logout
from Radiology.models import *


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            login(request, user)
            return HttpResponseRedirect('/home/')
    else:
        form = LoginForm()
    return render(request, "login.html", {'form': form})

@login_required
def home(request):
    person = Person.objects.get(user__username=request.user.username)
    return render(request, 'home.html', {'person':person})

@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/login/')