from jsonview.decorators import json_view
from bdiadmin.models import District
from django.http import JsonResponse
import json

@json_view
def get_district(request, pk):

    district = []
    for i in District.objects.filter(province=pk).values('id', 'name'):
        district.append({i['id']: i['name']})
    return JsonResponse(json.dumps(district), safe=False)

