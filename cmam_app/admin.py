from django.contrib import admin
from cmam_app.models import *
from import_export import resources
from import_export.admin import ExportMixin
from import_export import fields
from bdiadmin.models import *


class ProductAdminResource(resources.ModelResource):
    class Meta:
        model =Product
        fields = ('designation', 'general_measuring_unit', 'dose_par_semaine', 'quantite_en_stock_central')

class ProductAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = ProductAdminResource
    list_display = ('designation', 'general_measuring_unit', 'dose_par_semaine', 'quantite_en_stock_central')
    search_fields = ('designation', 'general_measuring_unit' )
    list_filter = ( 'dose_par_semaine',)


class FacilityAdminResource(resources.ModelResource):
    class Meta:
        model =Facility
        fields = ('id_facility', 'name', 'facility_level__name')

class FacilityAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = FacilityAdminResource
    list_display = ('id_facility', 'name', 'facility_level')
    search_fields = ('id_facility', 'name')
    list_filter = ( 'facility_level',)

class StockAdminResource(resources.ModelResource):
    class Meta:
        model =Stock
        fields = ('id_facility', 'product', 'quantity')

class StockAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = StockAdminResource
    list_display = ('id_facility', 'product', 'quantity')
    search_fields = ('id_facility', 'product')
    list_filter = ( 'product',)

class ReporterAdminResource(resources.ModelResource):
    class Meta:
        model = Reporter
        fields = ('facility', 'phone_number', 'supervisor_phone_number')

class ReporterAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = ReporterAdminResource
    list_display = ('facility', 'phone_number', 'supervisor_phone_number')
    search_fields = ('facility', 'phone_number', 'supervisor_phone_number')
    list_filter = ( 'facility__facility_level__name',)

class ReportAdminResource(resources.ModelResource):
    centrale = fields.Field()
    province = fields.Field()
    district = fields.Field()
    hospital = fields.Field()
    cds  = fields.Field()

    class Meta:
        model = Report
        fields = ('cds', 'hospital', 'centrale', 'district', 'province', 'reporting_date', 'text', 'category')

    def dehydrate_cds(self, report):
        if report.facility.facility_level.name in ["CDS", "Hospital"]:
            return report.facility.name
        return

    def dehydrate_district(self, report):
        if report.facility.facility_level.name in ["CDS", "Hospital"]:
            return CDS.objects.get(code = report.facility.id_facility).district.name
        elif report.facility.facility_level.name in ["District"]:
            return report.facility.name
        return

    def dehydrate_hospital(self, report):
        if report.facility.facility_level.name in ["Hospital"]:
            cds = CDS.objects.get(code = report.facility.id_facility)
            return cds.district.name
        return

    def dehydrate_province(self, report):
        if report.facility.facility_level.name in ["CDS", "Hospital"]:
            print report.facility.id_facility
            return CDS.objects.get(code = report.facility.id_facility).district.province.name
        elif report.facility.facility_level.name in ["District"]:
            return District.objects.get(code = int(report.facility.id_facility)).province.name
        elif report.facility.facility_level.name in ["Province"]:
            return report.facility.name
        return

    def dehydrate_centrale(self, report):
        if report.facility.facility_level.name in ["Centrale"]:
            return "Centale"
        return "Burundi"

class ReportAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = ReportAdminResource
    list_display = ('facility', 'reporting_date', 'text', 'category')
    search_fields = ('facility', 'reporting_date', 'text', 'category')
    list_filter = ( 'category', 'facility__facility_level')

class IncomingPatientsReportAdminResource(resources.ModelResource):
    class Meta:
        model = IncomingPatientsReport
        fields = ('total_debut_semaine', 'ptb','oedemes','rechute','readmission','transfert_interne','date_of_first_week_day', 'report__reporting_date', 'report__text', 'report__category', 'report__facility', 'report__facility__facility_level')

class IncomingPatientsReportAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = IncomingPatientsReportAdminResource
    list_display = ('total_debut_semaine', 'ptb','oedemes','rechute','readmission','transfert_interne','date_of_first_week_day', 'facility', 'type')
    search_fields = ('date_of_first_week_day', )
    list_filter = ( 'date_of_first_week_day', 'report__facility__facility_level')

    def facility(self, obj):
        return obj.report.facility

    def type(self, obj):
        return obj.report.facility.facility_level

class OutgoingPatientsReportAdminResource(resources.ModelResource):
    class Meta:
        model = OutgoingPatientsReport
        fields = ('gueri', 'deces', 'abandon', 'non_repondant', 'transfert_interne', 'date_of_first_week_day', 'report__reporting_date', 'report__text', 'report__category', 'report__facility', 'report__facility__facility_level')

class OutgoingPatientsReportAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = OutgoingPatientsReportAdminResource
    list_display = ('gueri', 'deces', 'abandon', 'non_repondant', 'transfert_interne', 'date_of_first_week_day', 'facility', 'type')
    search_fields = ('date_of_first_week_day', )
    list_filter = ( 'date_of_first_week_day', 'report__facility__facility_level')

    def facility(self, obj):
        return obj.report.facility

    def type(self, obj):
        return obj.report.facility.facility_level


admin.site.register(Product, ProductAdmin)
admin.site.register(Facility, FacilityAdmin)
admin.site.register(Stock, StockAdmin)
admin.site.register(Reporter, ReporterAdmin)
admin.site.register(User)
admin.site.register(Report, ReportAdmin)
admin.site.register(Sortie)
admin.site.register(Reception)
admin.site.register(StockOutReport)
admin.site.register(ProductsReceptionReport)
admin.site.register(ProductsTranferReport)
admin.site.register(IncomingPatientsReport, IncomingPatientsReportAdmin)
admin.site.register(OutgoingPatientsReport, OutgoingPatientsReportAdmin)
admin.site.register(StockReport)
admin.site.register(ProductStockReport)
admin.site.register(Temporary)
admin.site.register(FacilityType)
admin.site.register(FacilityTypeProduct)
