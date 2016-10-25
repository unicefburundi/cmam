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
from cmam_app.utils import get_adminqueryset, get_reportqueryset


@login_required
def get_year(request):
    dates = Report.objects.values('reporting_date').distinct().dates('reporting_date', 'year')
    years = {}
    for d in dates:
        years[d.year] = d.year
    return JsonResponse(years, safe=False)


@login_required
def get_week(request):
    dates = Report.objects.values('reporting_date').distinct().dates('reporting_date', 'day')
    weeks = {}
    for d in dates:
        weeks[d.strftime("%W")] = "W{0}".format(d.strftime("%W"))
    return JsonResponse(weeks, safe=False)


def landing(request):
    return render(request, 'landing_page.html')


@login_required(login_url="/login/")
def home(request):
    return render(request, "landing_page.html")


@login_required(login_url="/login/")
def dashboard(request):
    return render(request, "index.html")


@login_required(login_url="/login/")
def programs(request):
    return render(request, "cmam_app/programs.html")


class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to view or edit products.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class StockView(FormView):
    template_name = 'cmam_app/stocks.html'
    form_class = SortiesForm


class ProvinceDistrictViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to view or edit province.
    """
    queryset = Province.objects.all()
    serializer_class = ProvinceDistrictsSerializer

    def get_queryset(self):
        return get_adminqueryset(self.request, self.queryset)


class DistrictCDSViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to view or edit district.
    """
    queryset = District.objects.all()
    serializer_class = DistrictCDSSerializer
    lookup_field = 'code'

    def get_queryset(self):
        return get_adminqueryset(self.request, self.queryset)


class CDSCDSViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to view or edit district.
    """
    queryset = CDS.objects.all()
    serializer_class = CDSSerializers
    lookup_field = 'code'
    filter_fields = ('code', 'district__code', 'district__province__code')
    search_fields = ('^code',)

    def get_queryset(self):
        return get_adminqueryset(self.request, self.queryset)


class IncomingViewset(viewsets.ModelViewSet):
    """
    API endpoint that allows users to view or edit district.
    """
    queryset = IncomingPatientsReport.objects.all()
    serializer_class = IncomingPatientSerializer

    def get_queryset(self):
        return get_reportqueryset(self.request, self.queryset)


class OutgoingViewset(viewsets.ModelViewSet):
    """
    API endpoint that allows users to view or edit district.
    """
    queryset = OutgoingPatientsReport.objects.all()
    serializer_class = OutgoingPatientSerializer

    def get_queryset(self):
        return get_reportqueryset(self.request, self.queryset)


class InOutViewset(viewsets.ModelViewSet):
    serializer_class = InOutSerialiser
    queryset = PatientReports.objects.all()
    filter_fields = ('facility__facility_level__name', 'date_of_first_week_day')
    search_fields = ('^facility__id_facility',)

    def get_queryset(self):
        return get_reportqueryset(self.request, self.queryset)


class SumOutgoingViewset(viewsets.ModelViewSet):
    """
    API endpoint that allows users to view or edit district.
    """
    queryset = OutgoingPatientsReport.objects.all()
    serializer_class = SumOutSerialiser
    filter_fields = ('report__facility__facility_level__name', )
    search_fields = ('^report__facility__id_facility',)

    def get_queryset(self):
        return get_reportqueryset(self.request, self.queryset)
