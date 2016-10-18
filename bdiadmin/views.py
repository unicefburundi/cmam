from jsonview.decorators import json_view
from bdiadmin.models import District, Province, ProfileUser
from bdiadmin.serializers import ProvinceSerializer, DistrictSerializer
from django.http import JsonResponse
import json
from django.shortcuts import render, HttpResponseRedirect
from rest_framework import viewsets
from bdiadmin.forms import *
from django.contrib.auth.decorators import login_required
from django.forms.models import inlineformset_factory
from django.views.generic import ListView
from django.core.exceptions import PermissionDenied

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

@login_required
def edit_user(request, pk):
    user = User.objects.get(pk=pk)
    user_form = ProfileUserForm(instance=user)

    ProfileInlineFormset = inlineformset_factory(User, ProfileUser, fields=('telephone', 'level'))
    formset = ProfileInlineFormset(instance=user)

    if request.user.is_authenticated() and request.user.id == user.id:
        if request.method == "POST":
            user_form = ProfileUserForm(request.POST, instance=user)
            formset = ProfileInlineFormset(request.POST, instance=user)

            if user_form.is_valid():
                created_user = user_form.save(commit=False)
                formset = ProfileInlineFormset(request.POST, request.FILES, instance=created_user)

                if formset.is_valid():
                    created_user.save()
                    formset.save()
                    return HttpResponseRedirect('/bdiadmin/profile/')

        return render(request, "bdiadmin/account_update.html", {
            "noodle": pk,
            "noodle_form": user_form,
            "formset": formset,
        })
    else:
        raise PermissionDenied

class ProfileUserListView(ListView):
    model = ProfileUser
    paginate_by = 25