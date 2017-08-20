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
from django.http import HttpResponse
import json
import datetime
from datetime import datetime

NOWYEAR = datetime.today().year

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
    d = {}
    data = ["BAL", "ADM", "STR"]
    d['reportingcategories'] = data
    
    return render(request, "index.html", d)
    
    
@login_required
def fetchweeks(request):
    d = {}
    yearselected = request.GET["yearselected"]
    weekslist = []
    if (yearselected.isdigit()):
        weeks = abs(((datetime.strptime(str(yearselected) + "-12" + "-31", "%Y-%m-%d")) - (datetime.strptime(str(yearselected) + "-1" + "-1", "%Y-%m-%d"))).days/7)
        
        for w in range(0, weeks):
            weekslist.append(w+1)
    d["weeks"] = weekslist
    response_data = json.dumps(d)
    return HttpResponse(response_data, content_type="application/json")
    
    
@login_required
def fetchreportingrates(request):
    d = {}
    yearselected = request.GET["yearselected"]
    weekid = request.GET["week"]
    provinceid = request.GET["provinceid"]
    districtid = request.GET["districtid"]
    cdsid = request.GET["cdsid"]
    ratecategoryid = request.GET["ratecategoryid"]
    
    recnumber = 0
    recnumberList = []
    areatype = ""
    cdslist = None
    exepectednumber = 0
    noofweeks = 0
    
    lowestreportdate = Report.objects.all().order_by('-reporting_date')[0]
    if (lowestreportdate):
        lowestreportdate = datetime.strptime(str(lowestreportdate.reporting_date), "%Y-%m-%d")
        
    highestreportdate = Report.objects.all().order_by('reporting_date')[0]
    if (highestreportdate):
        highestreportdate = datetime.strptime(str(highestreportdate.reporting_date), "%Y-%m-%d")
        
    if (lowestreportdate and highestreportdate):
        noofweeks = abs((highestreportdate - lowestreportdate).days/7)
    
    if (cdsid.isdigit()):
        cdslistids = CDS.objects.values_list("code" , flat=True).get(code = cdsid)
        facilitylist = Facility.objects.filter(id_facility__in = cdslistids)
        cdslist = CDS.objects.get(code = cdsid)
        if (yearselected.isdigit()):
            if (weekid.isdigit()):
                data = Report.objects.filter(text__icontains=ratecategoryid, reporting_date__year = yearselected, facility__in = facilitylist)
                noofweeks = 1
                for b in data:
                    if (b.reporting_date.isocalendar()[1] == int(weekid)):
                        recnumber += 1
            else:
                if datetime.now().year == yearselected:
                    noofweeks = datetime.now().isocalendar()[1]
                else:
                    noofweeks = abs(((datetime.strptime(str(yearselected) + "-12" + "-31", "%Y-%m-%d")) - (datetime.strptime(str(yearselected) + "-1" + "-1", "%Y-%m-%d"))).days/7)
                    
                recnumber = Report.objects.filter(text__icontains=ratecategoryid, reporting_date__year = yearselected, facility__in = facilitylist).count()/noofweeks
            
        else:
            recnumber = Report.objects.filter(text__icontains=ratecategoryid, facility__in = facilitylist).count()/noofweeks
            
        exepectednumber = 1
        recnumberList.append([cdslist.code, cdslist.name, recnumber, exepectednumber])
        areatype = "CDS"
        
    elif (districtid.isdigit()):
        districtlist = District.objects.get(code = districtid)
        if (districtlist):
            cdslist = CDS.objects.filter(district = districtlist)
            for cds in cdslist.iterator():
                cdslistids = CDS.objects.values_list("code" ,flat=True).filter(code = cds.code)
                facilitylist = Facility.objects.filter(id_facility__in = cdslistids)
                recnumber = 0
                if (yearselected.isdigit()):
                    if (weekid.isdigit()):
                        data = Report.objects.filter(text__icontains=ratecategoryid, reporting_date__year = yearselected, facility__in = facilitylist)
                        noofweeks = 1
                        for b in data:
                            if (b.reporting_date.isocalendar()[1] == int(weekid)):
                                recnumber += 1
                    else:
                        if datetime.now().year == yearselected:
                            noofweeks = datetime.now().isocalendar()[1]
                        else:
                            noofweeks = abs(((datetime.strptime(str(yearselected) + "-12" + "-31", "%Y-%m-%d")) - (datetime.strptime(str(yearselected) + "-1" + "-1", "%Y-%m-%d"))).days/7)
                            
                        recnumber += Report.objects.filter(text__icontains=ratecategoryid, reporting_date__year = yearselected, facility__in = facilitylist).count()/noofweeks
                        
                else:
                    recnumber += Report.objects.filter(text__icontains=ratecategoryid, facility__in = facilitylist).count()/noofweeks
                
                exepectednumber = 1
                recnumberList.append([cds.code, cds.name, recnumber, exepectednumber])
        areatype = "CDS"
        
    elif (provinceid.isdigit()):
        provincelist = Province.objects.get(code = provinceid)
        if (provincelist):
            districtlist = District.objects.filter(province = provincelist)
            if (districtlist):
                for dist in districtlist.iterator():
                    recnumber = 0
                    exepectednumber = 0
                    cdslistids = CDS.objects.values_list("code" , flat=True).filter(district = dist)
                    facilitylist = Facility.objects.filter(id_facility__in = cdslistids)
                    #cdslist = CDS.objects.filter(district = dist)
                    if (yearselected.isdigit()):
                        if (weekid.isdigit()):
                            data = Report.objects.filter(text__icontains=ratecategoryid, reporting_date__year = yearselected, facility__in = facilitylist)
                            noofweeks = 1
                            for b in data:
                                if (b.reporting_date.isocalendar()[1] == int(weekid)):
                                    recnumber += 1
                        else:
                            if datetime.now().year == yearselected:
                                noofweeks = datetime.now().isocalendar()[1]
                            else:
                                noofweeks = abs(((datetime.strptime(str(yearselected) + "-12" + "-31", "%Y-%m-%d")) - (datetime.strptime(str(yearselected) + "-1" + "-1", "%Y-%m-%d"))).days/7)
                                
                            recnumber += Report.objects.filter(text__icontains=ratecategoryid, reporting_date__year = yearselected, facility__in = facilitylist).count()/noofweeks
                            
                    else:
                        recnumber += Report.objects.filter(text__icontains=ratecategoryid, facility__in = facilitylist).count()/noofweeks
                    
                    exepectednumber += facilitylist.count()
                    recnumberList.append([dist.code, dist.name, recnumber, exepectednumber])
        areatype = "District"
                    
    else:
        provincelist = Province.objects.all()
        if (provincelist):
            for prov in provincelist.iterator():
                recnumber = 0
                exepectednumber = 0
                districtlist = District.objects.filter(province = prov)
                if (districtlist):
                    for dist in districtlist.iterator():
                        cdslistids = CDS.objects.values_list("code" , flat=True).filter(district = dist)
                        facilitylist = Facility.objects.filter(id_facility__in = cdslistids)
                        #cdslist = CDS.objects.filter(district = dist)
                        if (yearselected.isdigit()):
                            if (weekid.isdigit()):
                                data = Report.objects.filter(text__icontains=ratecategoryid, reporting_date__year = yearselected, facility__in = facilitylist)
                                noofweeks = 1
                                for b in data:
                                    if (b.reporting_date.isocalendar()[1] == int(weekid)):
                                        recnumber += 1
                            else:
                                if datetime.now().year == yearselected:
                                    noofweeks = datetime.now().isocalendar()[1]
                                else:
                                    noofweeks = abs(((datetime.strptime(str(yearselected) + "-12" + "-31", "%Y-%m-%d")) - (datetime.strptime(str(yearselected) + "-1" + "-1", "%Y-%m-%d"))).days/7)
        
                                recnumber += Report.objects.filter(text__icontains=ratecategoryid, reporting_date__year = yearselected, facility__in = facilitylist).count()/noofweeks
                                
                        else:
                            recnumber += Report.objects.filter(text__icontains=ratecategoryid, facility__in = facilitylist).count()/noofweeks
                            
                        exepectednumber += facilitylist.count()
                recnumberList.append([prov.code, prov.name, recnumber, exepectednumber])
        areatype = "Province"
        
    d['areatype'] = areatype
    d['receivednumberlist'] = recnumberList
    
    response_data = json.dumps(d)
    return HttpResponse(response_data, content_type="application/json")
    

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

    def get_serializer_context(self):
        YEAR = datetime.today().year
        if self.request.GET.get('year'):
            YEAR = self.request.GET['year']    
        return {'YEAR': YEAR}


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
    queryset = PatientReports.objects.all()
    serializer_class = InOutSerialiser
    filter_fields = ('facility__facility_level__name', 'date_of_first_week_day')
    search_fields = ('^facility__id_facility',)

    def get_queryset(self):
        YEAR = datetime.today().year
        if self.request.GET.get('year'):
            YEAR = self.request.GET['year']    
        self.queryset = self.queryset.filter(date_of_first_week_day__year=YEAR)
        return get_reportqueryset(self.request, self.queryset)


class SumOutgoingViewset(viewsets.ModelViewSet):
    """
    API endpoint that allows users to view or edit district.
    """
    queryset = OutgoingPatientsReport.objects.all()
    serializer_class = SumOutSerialiser
    filter_fields = ('report__facility__facility_level__name', 'date_of_first_week_day')
    search_fields = ('^report__facility__id_facility',)

    def get_queryset(self):
        YEAR = datetime.today().year
        if self.request.GET.get('year'):
            YEAR = self.request.GET['year']    
        self.queryset = self.queryset.filter(date_of_first_week_day__year=YEAR)
        return get_reportqueryset(self.request, self.queryset)
