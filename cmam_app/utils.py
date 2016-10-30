from bdiadmin.models import ProfileUser
from django.contrib.auth.decorators import login_required
from cmam_app.models import PatientReports


@login_required(login_url="/login/")
def get_adminqueryset(request, queryset, **kwargs):
    if request.user.is_superuser:
        return queryset
    else:
        profile, created = ProfileUser.objects.get_or_create(user=request.user)
        if created:
            print "created"
        elif profile.level:
            queryset = queryset.filter(code__startswith=profile.level)
            return queryset


@login_required(login_url="/login/")
def get_reportqueryset(request, queryset, **kwargs):
    if request.user.is_superuser:
        return queryset
    else:
        profile, created = ProfileUser.objects.get_or_create(user=request.user)
        if created:
            print "created"
        elif profile.level:
            if queryset.model is PatientReports:
                return queryset.filter(facility__id_facility__startswith=profile.level)
            else:
                return queryset.filter(report__facility__id_facility__startswith=profile.level)
