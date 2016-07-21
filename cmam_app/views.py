#-*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from cmam_app.models import Product
from cmam_app.serializers import ProductSerializer
from django.views.generic.edit import FormView
from cmam_app.forms import SortiesForm



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

class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to view or edit products.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class SortiesView(FormView):
    template_name = 'cmam_app/sorties.html'
    form_class = SortiesForm

