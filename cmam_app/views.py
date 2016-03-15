#-*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse


def test(request):
	text = """<h1> TEST !"""
	#return HttpResponse(request, 'cmam_app/test.html', locals())
	return HttpResponse(text)


def landing(request):
    return render(request, 'landing_page.html')
