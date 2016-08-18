#-*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from cmam_app.models import *
from cmam_app.serializers import *
from bdiadmin.models import Province, District
from django.views.generic.edit import FormView
from cmam_app.forms import SortiesForm
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework import status
from django.contrib import messages
from django.db.models.functions import Coalesce
from django.db.models import Sum
import itertools


@login_required
def get_year(request):
    dates = Report.objects.values('reporting_date').distinct().dates('reporting_date', 'year')
    years = {}
    for d in dates:
        years[d.year] = d.year
    return JsonResponse(years, safe=False)



def landing(request):
    return render(request, 'landing_page.html')


@login_required(login_url="login/")
def home(request):
    return render(request, "landing_page.html")

@login_required(login_url="login/")
def dashboard(request):
    return render(request, "index.html")

@login_required(login_url="login/")
def programs(request):
    return render(request, "cmam_app/programs.html")

class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to view or edit products.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_context_data(self, **kwargs):
        context = super(ProductViewSet, self).get_context_data(**kwargs)
        return context


class StockView(FormView):
    template_name = 'cmam_app/stocks.html'
    form_class = SortiesForm

    def get_context_data(self, **kwargs):
        context = super(SortiesView, self).get_context_data(**kwargs)
        for p in Product.objects.all():
            sorties_central = ProductsTranferReport.objects.filter(produit=p, sortie__report__facility__facility_level__name='Centrale' ).aggregate(sortie=Coalesce(Sum('quantite_donnee'), 0))['sortie']
            sorties_district = ProductsTranferReport.objects.filter(produit=p, sortie__report__facility__facility_level__name='District' ).aggregate(sortie=Coalesce(Sum('quantite_donnee'), 0))['sortie']
            entrees_district = ProductsReceptionReport.objects.filter(produit=p , reception__report__facility__facility_level__name='District').aggregate(reception=Coalesce( Sum('quantite_recue'), 0))['reception']
            entrees_cds = ProductsReceptionReport.objects.filter(produit=p , reception__report__facility__facility_level__name='CDS').aggregate(reception=Coalesce( Sum('quantite_recue'), 0))['reception']
            entrees_hospital = ProductsReceptionReport.objects.filter(produit=p , reception__report__facility__facility_level__name='Hospital').aggregate(reception=Coalesce( Sum('quantite_recue'), 0))['reception']

            if  sorties_central != entrees_district:
                messages.add_message(self.request, messages.INFO, 'Les sorties central ({0})  sont differentes des entrees district ({1}) pour le {2}!'.format(sorties_central, entrees_district, p))
            if  sorties_district != (entrees_cds + entrees_hospital):
                messages.add_message(self.request, messages.INFO, 'Les sorties districts ({0})  sont differentes des entrees cds ({1}) et hospitaux ({2}) pour le {3}!'.format(sorties_district, entrees_cds, entrees_hospital, p))
        return context

class ProvinceDistrictViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to view or edit province.
    """
    queryset = Province.objects.all()
    serializer_class = ProvinceDistrictsSerializer

    # For get provinces
    @detail_route(methods=['get'], url_path='(?P<product>\d+)')
    def update_product(self, request, pk, product=None):
        """ Updates the object identified by the pk ans add the product """
        queryset = Province.objects.filter(pk=pk)
        serializer = ProvinceDistrictsSerializer(queryset, many=True, context={'product': product})
        return Response(serializer.data, status=status.HTTP_200_OK)

class DistrictCDSViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to view or edit district.
    """
    queryset = District.objects.all()
    serializer_class = DistrictCDSSerializer
    lookup_field = 'code'

    # For get districts
    @detail_route(methods=['get'], url_path='(?P<product>\d+)')
    def update_product(self, request, pk, product=None):
        """ Updates the object identified by the pk ans add the product """
        queryset = District.objects.filter(code=pk)
        serializer = DistrictCDSSerializer(queryset, many=True, context={'product': product})
        return Response(serializer.data, status=status.HTTP_200_OK)


class InOutPatientsViewset(viewsets.ModelViewSet):
    """
    API endpoint that lists all In/Out patients.
    """
    def list(self, request):
        queryset = list(itertools.chain(IncomingPatientsReport.objects.all(), OutgoingPatientsReport.objects.all()))
        serializer = InOutPatientSerializer(queryset, many=True)
        return Response(serializer.data)