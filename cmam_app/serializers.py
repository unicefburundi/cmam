from rest_framework import serializers
from cmam_app.models import *
from django.db.models import Sum
from django.db.models.functions import Coalesce
from bdiadmin.serializers import ProvinceSerializer
from bdiadmin.models import Province, District, CDS


class ProductSerializer(serializers.ModelSerializer):
    """ Serializer to represent the Product model """
    reception = serializers.SerializerMethodField()
    sortie = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ("id", "designation", "quantite_en_stock_central", "general_measuring_unit", 'reception', 'sortie')

    def get_reception(self, obj):
        reception = ProductsReceptionReport.objects.filter(produit=obj , reception__report__facility__facility_level__name='Centrale').aggregate(reception=Coalesce(Sum('quantite_recue'), 0))
        return reception['reception']

    def get_sortie(self, obj):
        sortie = ProductsTranferReport.objects.filter(produit=obj, sortie__report__facility__facility_level__name='Centrale').aggregate(sortie=Coalesce(Sum('quantite_donnee'), 0))
        return sortie['sortie']


class ProvinceDistrictsSerializer(ProvinceSerializer):
    """ show not only the province but also the districts into that province"""
    districts = serializers.SerializerMethodField()

    class Meta:
        model = Province
        fields = ("name", "code", "districts")

    def get_districts(self, obj):
        districts = District.objects.filter(province__code=obj.code).values('name', 'code')
        for d in districts:
            for p in Product.objects.all():
                d[p.designation] = {}
                d[p.designation]['reception'] = ProductsReceptionReport.objects.filter(produit=p, reception__report__facility__id_facility=d['code']).aggregate(reception=Coalesce(Sum('quantite_recue'), 0))['reception']
                d[p.designation]['sortie'] = ProductsTranferReport.objects.filter(produit=p, sortie__report__facility__id_facility=d['code']).aggregate(sortie=Coalesce(Sum('quantite_donnee'), 0))['sortie']
        return districts


class DistrictCDSSerializer(ProvinceSerializer):
    """ show not only the province but also the districts into that province"""
    cds = serializers.SerializerMethodField()

    class Meta:
        model = District
        fields = ("name", "code", "cds")

    def get_cds(self, obj):
        cds = CDS.objects.filter(district__code=obj.code).values('name', 'code')
        for d in cds:
            for p in Product.objects.all():
                d[p.designation] = {}
                d[p.designation]['reception'] = ProductsReceptionReport.objects.filter(produit=p, reception__report__facility__id_facility=d['code']).aggregate(reception=Coalesce( Sum('quantite_recue'), 0))['reception']
                d[p.designation]['sortie'] = ProductsTranferReport.objects.filter(produit=p, sortie__report__facility__id_facility=d['code']).aggregate(sortie=Coalesce(Sum('quantite_donnee'), 0))['sortie']

        return cds


class CDSSerializers(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()

    class Meta:
        model = CDS
        fields = ("products", "name", "code")

    def get_products(self, obj):
        cds = CDS.objects.filter(code=obj.code).values('name', 'code')
        for d in cds:
            for p in Product.objects.all():
                d[p.designation] = {}
                d[p.designation]['reception'] = ProductsReceptionReport.objects.filter(produit=p, reception__report__facility__id_facility=d['code']).aggregate(reception=Coalesce(Sum('quantite_recue'), 0))['reception']
                d[p.designation]['sortie'] = ProductsTranferReport.objects.filter(produit=p, sortie__report__facility__id_facility=d['code']).aggregate(sortie=Coalesce(Sum('quantite_donnee'), 0))['sortie']

        return cds


class IncomingPatientSerializer(serializers.ModelSerializer):

    class Meta:
        model = IncomingPatientsReport
        fields = ('total_debut_semaine', 'ptb', 'oedemes', 'rechute','readmission','transfert_interne_i','date_of_first_week_day')


class OutgoingPatientSerializer(serializers.ModelSerializer):

    class Meta:
        model = OutgoingPatientsReport
        fields = ('gueri','deces','abandon','non_repondant','transfert_interne_o','date_of_first_week_day')


class InOutSerialiser(serializers.Serializer):
    week = serializers.CharField()
    total_debut_semaine = serializers.IntegerField(default=0)
    ptb = serializers.IntegerField(default=0)
    oedemes = serializers.IntegerField(default=0)
    rechute = serializers.IntegerField(default=0)
    readmission = serializers.IntegerField(default=0)
    transfert_interne_i = serializers.IntegerField(default=0)
    date_of_first_week_day = serializers.DateField()
    gueri = serializers.IntegerField(default=0)
    deces = serializers.IntegerField(default=0)
    abandon = serializers.IntegerField(default=0)
    non_repondant = serializers.IntegerField(default=0)
    transfert_interne_o = serializers.IntegerField(default=0)
    facility = serializers.CharField()


class SumOutSerialiser(serializers.ModelSerializer):
    week = serializers.SerializerMethodField()

    class Meta:
        model = OutgoingPatientsReport
        fields = ('gueri','deces','abandon', "week",)

    def get_week(self, obj):
        return "W{0}".format(obj.date_of_first_week_day.strftime("%W"))

