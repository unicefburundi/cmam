from django.contrib import admin
from cmam_app.models import *
from import_export import resources
from import_export.admin import ExportMixin

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
    class Meta:
        model = Report
        fields = ('facility', 'reporting_date', 'text', 'category')

class ReportAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = ReportAdminResource
    list_display = ('facility', 'reporting_date', 'text', 'category')
    search_fields = ('facility', 'reporting_date', 'text', 'category')
    list_filter = ( 'category',)


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
admin.site.register(IncomingPatientsReport)
admin.site.register(OutgoingPatientsReport)
admin.site.register(StockReport)
admin.site.register(ProductStockReport)
admin.site.register(Temporary)
admin.site.register(FacilityType)
admin.site.register(FacilityTypeProduct)
