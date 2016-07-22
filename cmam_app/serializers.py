from rest_framework import serializers
from cmam_app.models import Product


class ProductSerializer(serializers.ModelSerializer):
    """ Serializer to represent the Product model """
    class Meta:
        model = Product
        fields = ("designation", "quantite_en_stock_central", "general_measuring_unit")