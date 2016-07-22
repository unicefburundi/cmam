from rest_framework import serializers
from bdiadmin.models import Province, District


class ProvinceSerializer(serializers.ModelSerializer):
    """ Serializer to represent the Province model """
    class Meta:
        model = Province
        fields = ("name", "code")

class DistrictSerializer(serializers.ModelSerializer):
    """ Serializer to represent the District model """
    class Meta:
        model = District
        fields = ("name", "code", "province")
