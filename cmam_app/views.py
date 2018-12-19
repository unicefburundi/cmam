# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from cmam_app.models import *
from cmam_app.serializers import *
from bdiadmin.models import Province, District
from django.views.generic.edit import FormView
from django.views.generic.base import TemplateView
from cmam_app.utils import get_adminqueryset, get_reportqueryset
from django.http import HttpResponse
import json
from datetime import datetime

NOWYEAR = datetime.today().year


@login_required
def get_year(request):
    dates = (
        Report.objects.values("reporting_date")
        .distinct()
        .dates("reporting_date", "year")
    )
    years = {}
    for d in dates:
        years[d.year] = d.year
    return JsonResponse(years, safe=False)


@login_required
def get_week(request):
    dates = (
        Report.objects.values("reporting_date")
        .distinct()
        .dates("reporting_date", "day")
    )
    weeks = {}
    for d in dates:
        weeks[d.strftime("%W")] = "W{0}".format(d.strftime("%W"))
    return JsonResponse(weeks, safe=False)


def landing(request):
    return render(request, "landing_page.html")


@login_required(login_url="/login/")
def home(request):
    return render(request, "landing_page.html")


@login_required(login_url="/login/")
def dashboard(request):
    d = {}
    data = ["BAL", "ADM", "STR"]
    d["reportingcategories"] = data
    return render(request, "index.html", d)


@login_required(login_url="/login/")
def detailscds(request, code=None):
    data = {}
    data["Report"] = Report.objects.filter(facility__id_facility=code)
    data["ProductsReceptionReport"] = ProductsReceptionReport.objects.filter(
        reception__report__facility__id_facility=code
    )
    data["ProductsTranferReport"] = ProductsTranferReport.objects.filter(
        sortie__report__facility__id_facility=code
    )
    data["ProductStockReport"] = ProductStockReport.objects.filter(
        stock_report__report__facility__id_facility=code
    )
    data["StockOutReport"] = StockOutReport.objects.filter(
        report__facility__id_facility=code
    )
    data["Facility"] = Facility.objects.get(id_facility=code)
    return render(request, "cmam_app/details.html", data)


@login_required(login_url="/login/")
def programs(request):
    return render(request, "cmam_app/programs.html")


class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to view or edit products.
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class StockView(TemplateView):
    template_name = "cmam_app/stocks.html"


class ProvinceDistrictViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to view or edit province.
    """

    queryset = Province.objects.all().prefetch_related("district_set")
    serializer_class = ProvinceDistrictsSerializer

    def get_queryset(self):
        return get_adminqueryset(self.request, self.queryset)

    def get_serializer_context(self):
        YEAR = datetime.today().year
        if self.request.GET.get("year"):
            YEAR = self.request.GET["year"]
        return {"YEAR": YEAR}


class DistrictCDSViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to view or edit district.
    """

    queryset = District.objects.all().prefetch_related("cds_set")
    serializer_class = DistrictCDSSerializer
    lookup_field = "code"

    def get_queryset(self):
        return get_adminqueryset(self.request, self.queryset)


class CDSCDSViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to view or edit cds.
    """

    queryset = CDS.objects.filter(functional=True)
    serializer_class = CDSSerializers
    lookup_field = "code"
    filter_fields = ("code", "district__code", "district__province__code")
    search_fields = ("^code",)

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
    queryset = PatientReports.objects.all().select_related("facility__facility_level")
    serializer_class = InOutSerialiser
    filter_fields = ("facility__facility_level__name", "date_of_first_week_day")
    search_fields = ("^facility__id_facility",)

    def get_queryset(self):
        startdate = self.request.GET.get("startdate", "")
        enddate = self.request.GET.get("enddate", "")
        if startdate and startdate != "undefined":
            self.queryset = self.queryset.filter(
                date_of_first_week_day__gte=datetime.strptime(startdate, "%Y-%m-%d")
            )
        if enddate and enddate != "undefined":
            self.queryset = self.queryset.filter(
                date_of_first_week_day__lte=datetime.strptime(enddate, "%Y-%m-%d")
            )
        else:
            self.queryset = self.queryset.filter(
                date_of_first_week_day__year=datetime.today().year
            )
        return get_reportqueryset(self.request, self.queryset)


class SumOutgoingViewset(viewsets.ModelViewSet):
    """
    API endpoint that allows users to view or edit district.
    """

    queryset = OutgoingPatientsReport.objects.all().select_related("report__facility__facility_level")
    serializer_class = SumOutSerialiser
    filter_fields = ("report__facility__facility_level__name", "date_of_first_week_day")
    search_fields = ("^report__facility__id_facility",)

    def get_queryset(self):
        startdate = self.request.GET.get("startdate", "")
        enddate = self.request.GET.get("enddate", "")
        if startdate and startdate != "undefined":
            self.queryset = self.queryset.filter(
                date_of_first_week_day__gte=datetime.strptime(startdate, "%Y-%m-%d")
            )
        if enddate and enddate != "undefined":
            self.queryset = self.queryset.filter(
                date_of_first_week_day__lte=datetime.strptime(enddate, "%Y-%m-%d")
            )
        else:
            self.queryset = self.queryset.filter(
                date_of_first_week_day__year=datetime.today().year
            )
        return get_reportqueryset(self.request, self.queryset)
