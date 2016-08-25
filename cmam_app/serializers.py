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
        fields = ("id", "designation", "quantite_en_stock_central", "general_measuring_unit",  'reception', 'sortie')

    def get_reception(self, obj):
        reception = ProductsReceptionReport.objects.filter(produit=obj , reception__report__facility__facility_level__name='Centrale').aggregate(reception=Coalesce( Sum('quantite_recue'), 0))
        return reception['reception']


    def get_sortie(self, obj):
        sortie = ProductsTranferReport.objects.filter(produit=obj, sortie__report__facility__facility_level__name='Centrale' ).aggregate(sortie=Coalesce(Sum('quantite_donnee'), 0))
        return sortie['sortie']

class ProvinceDistrictsSerializer(ProvinceSerializer):
    """ show not only the province but also the districts into that province"""
    districts = serializers.SerializerMethodField()

    class Meta:
        model = Province
        fields = ("name", "code", "districts")

    def get_districts(self, obj):
        districts = District.objects.filter(province__code=obj.code).values('name', 'code')
        if self.context.get('product'):
            for d in districts:
                product = int(self.context.get('product'))
                d['reception'] = ProductsReceptionReport.objects.filter(produit=product, reception__report__facility__id_facility=d['code'] ).aggregate(reception=Coalesce( Sum('quantite_recue'), 0))['reception']
                d['sortie'] = ProductsTranferReport.objects.filter(produit=product, sortie__report__facility__id_facility=d['code']).aggregate(sortie=Coalesce( Sum('quantite_donnee'), 0))['sortie']
        return districts

class DistrictCDSSerializer(ProvinceSerializer):
    """ show not only the province but also the districts into that province"""
    cds = serializers.SerializerMethodField()

    class Meta:
        model = District
        fields = ("name", "code", "cds")

    def get_cds(self, obj):
        cds = CDS.objects.filter(district__code=obj.code).values('name', 'code')
        if self.context.get('product'):
            for d in cds:
                product = int(self.context.get('product'))
                d['reception'] = ProductsReceptionReport.objects.filter(produit=product, reception__report__facility__id_facility=d['code'] ).aggregate(reception=Coalesce( Sum('quantite_recue'), 0))['reception']
                d['sortie'] = ProductsTranferReport.objects.filter(produit=product, sortie__report__facility__id_facility=d['code'] ).aggregate(sortie=Coalesce( Sum('quantite_donnee'), 0))['sortie']

        return cds

class IncomingPatientSerializer(serializers.ModelSerializer):

    class Meta:
        model = IncomingPatientsReport
        fields = ('total_debut_semaine','ptb','oedemes','rechute','readmission','transfert_interne','date_of_first_week_day')

class OutgoingPatientSerializer(serializers.ModelSerializer):

    class Meta:
        model = OutgoingPatientsReport
        fields = ('gueri','deces','abandon','non_repondant','transfert_interne','date_of_first_week_day')

