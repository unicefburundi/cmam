from django import forms
from bdiadmin.models import *
from django.conf import settings
from django.utils.translation import ugettext as _

User = settings.AUTH_USER_MODEL


class ProvinceForm(forms.ModelForm):
    class Meta:
        model = Province
        fields = ('name', 'code')

class CommuneForm(forms.ModelForm):
    class Meta:
        model = Commune
        fields = ('province', 'name', 'code')

class CollineForm(forms.ModelForm):
    class Meta:
        model = Colline
        fields = ('commune','name', 'code')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

