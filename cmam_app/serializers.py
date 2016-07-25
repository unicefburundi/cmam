from rest_framework import serializers
from cmam_app.models import ProductsReceptionReport, ProductsTranferReport, Product
from django.db.models import Sum
from django.db.models.functions import Coalesce


class ProductSerializer(serializers.ModelSerializer):
    """ Serializer to represent the Product model """
    reception = serializers.SerializerMethodField()
    sortie = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ("designation", "quantite_en_stock_central", "general_measuring_unit",  'reception', 'sortie')

    def get_reception(self, obj):
        reception = ProductsReceptionReport.objects.filter(produit=obj ).aggregate(sortie=Coalesce( Sum('quantite_recue'), 0))
        return reception['sortie']


    def get_sortie(self, obj):
        sortie = ProductsTranferReport.objects.filter(produit=obj ).aggregate(reception=Coalesce(Sum('quantite_donnee'), 0))
        return sortie['reception']