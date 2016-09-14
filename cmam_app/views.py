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
from drf_multiple_model.mixins import MultipleModelMixin, Query


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
    def update_product(self, request, code, product=None):
        """ Updates the object identified by the pk ans add the product """
        queryset = District.objects.filter(code=code)
        serializer = DistrictCDSSerializer(queryset, many=True, context={'product': product})
        return Response(serializer.data, status=status.HTTP_200_OK)

class IncomingViewset(viewsets.ModelViewSet):
    """
    API endpoint that allows users to view or edit district.
    """
    queryset = IncomingPatientsReport.objects.all()
    serializer_class = IncomingPatientSerializer

class OutgoingViewset(viewsets.ModelViewSet):
    """
    API endpoint that allows users to view or edit district.
    """
    queryset = OutgoingPatientsReport.objects.all()
    serializer_class = OutgoingPatientSerializer

class InOutViewset(MultipleModelMixin, viewsets.ModelViewSet):
    serializer_class = InOutSerialiser

    queryList = (
        (IncomingPatientsReport.objects.all(), IncomingPatientSerializer),
        (OutgoingPatientsReport.objects.all(), OutgoingPatientSerializer),
        )

    def list(self, request, *args, **kwargs):
        # import ipdb; ipdb.set_trace()
        queryList = self.get_queryList()

        # Iterate through the queryList, run each queryset and serialize the data
        results = []
        for query in queryList:
            if not isinstance(query, Query):
                query = Query.new_from_tuple(query)
            # Run the queryset through Django Rest Framework filters
            queryset = query.queryset.all()
            queryset = self.filter_queryset(queryset)

            # If there is a user-defined filter, run that too.
            if query.filter_fn is not None:
                queryset = query.filter_fn(queryset, request, *args, **kwargs)

            # Run the paired serializer
            context = self.get_serializer_context()
            data = query.serializer(queryset, many=True, context=context).data

            results = self.format_data(data, query, results)

        if self.flat:
            # Sort by given attribute, if sorting_attribute is provided
            if self.sorting_field:
                results = self.queryList_sort(results)

            # Return paginated results if pagination is enabled
            page = self.paginate_queryList(results)
            if page is not None:
                return self.get_paginated_response(page)

        if request.accepted_renderer.format == 'html':
            return Response({'data': results})
        income = results[0]['incomingpatientsreport']
        outgon = results[1]['outgoingpatientsreport']

        for i in income:
            for o in outgon:
                if i['date_of_first_week_day'] == o['date_of_first_week_day']:
                    i.update(o)
                    outgon.remove(o)
        results = income + outgon
        return Response(results)
