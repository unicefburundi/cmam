from django import forms
from djng.styling.bootstrap3.forms import Bootstrap3Form
from cmam_app.models import Product
from bdiadmin.models import Province, District
# from djng.forms import NgFormValidationMixin

class SortiesForm(Bootstrap3Form):
    product = forms.ModelChoiceField(queryset=Product.objects.all(), error_messages={'invalid': 'Please select one product.'})
    province = forms.ModelChoiceField(queryset=Province.objects.all(), error_messages={'invalid': 'Please select one product.'})
    district = forms.ModelChoiceField(queryset=District.objects.all(), error_messages={'invalid': 'Please select one product.'})

# class SortiesForm2(NgFormValidationMixin, SortieSimpleForm):
#     # Apart from an additional mixin class, the Form declaration from the
#     # 'Classic Subscription' view, has been reused here.
#     pass