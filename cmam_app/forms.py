from django import forms
from djng.styling.bootstrap3.forms import Bootstrap3Form
from cmam_app.models import Product
from bdiadmin.models import Province, District
from djng.forms import NgFormValidationMixin

class SortieSimpleForm(Bootstrap3Form):
    product = forms.ModelChoiceField(queryset=Product.objects.all(), error_messages={'invalid': 'Please select one product.'})
    province = forms.ModelChoiceField(queryset=Province.objects.all(), error_messages={'invalid': 'Please select one product.'})
    district = forms.ModelChoiceField(queryset=District.objects.none(), error_messages={'invalid': 'Please select one product.'})

class SortiesForm(NgFormValidationMixin, SortieSimpleForm):
    # Apart from an additional mixin class, the Form declaration from the
    # 'Classic Subscription' view, has been reused here.
    field_css_classes = {
        'product' : ["ng-click : raba()"],
        }