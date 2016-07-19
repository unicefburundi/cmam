#-*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


def test(request):
	text = """<h1> TEST !"""
	#return HttpResponse(request, 'cmam_app/test.html', locals())
	return HttpResponse(text)


def landing(request):
    return render(request, 'landing_page.html')


@login_required(login_url="login/")
def home(request):
    return render(request, "landing_page.html")

@login_required(login_url="login/")
def dashboard(request):
    return render(request, "landing_page.html")