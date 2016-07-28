from jsonview.decorators import json_view
from bdiadmin.models import District, Province
from bdiadmin.serializers import ProvinceSerializer, DistrictSerializer
from django.http import JsonResponse
import json
from rest_framework import viewsets


@json_view
def get_district(request, pk):

    district = []
    for i in District.objects.filter(province=pk).values('id', 'name'):
        district.append({i['id']: i['name']})
    return JsonResponse(json.dumps(district), safe=False)


class ProvinceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to view or edit products.
    """
    queryset = Province.objects.all()
    serializer_class = ProvinceSerializer

class DistrictViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to view or edit products.
    """
    queryset = District.objects.all()
    serializer_class = DistrictSerializer