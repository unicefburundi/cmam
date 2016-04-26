from jsonview.decorators import json_view
from bdiadmin.models import *
from django.http import JsonResponse
import json
from django.views.generic import CreateView, ListView
from bdiadmin.forms import *
from django.core.urlresolvers import reverse

@json_view
def get_commune(request, pk):

    communes = []
    for i in Commune.objects.filter(province=pk).values('id', 'name'):
        communes.append({i['id']: i['name']})
    return JsonResponse(json.dumps(communes), safe=False)


@json_view
def get_colline(request, pk):
    collines = []
    for i in Colline.objects.filter(commune=pk).values('id', 'name'):
        collines.append({i['id']: i['name']})
    return JsonResponse(json.dumps(collines), safe=False)

class ProvinceCreateView(CreateView):
    model = Province
    form_class = ProvinceForm

    def get_success_url(self):
        return reverse('bdiadmin:province_list')

class ProvinceListView(ListView):
    model = Province
    paginate_by = 100

class CommuneCreateView(CreateView):
    model = Commune
    form_class = CommuneForm

    def get_success_url(self):
        return reverse('bdiadmin:commune_list')

class CommuneListView(ListView):
    model = Commune
    paginate_by = 100


class CollineCreateView(CreateView):
    model = Colline
    form_class = CollineForm

    def get_success_url(self):
        return reverse('bdiadmin:colline_list')

class CollineListView(ListView):
    model = Colline
    paginate_by = 100