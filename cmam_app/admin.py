from django.contrib import admin
from cmam_app.models import (
    Product,
    PatientReports,
    IncomingPatientsReport,
    OutgoingPatientsReport,
    Reception,
    Report,
    Reporter,
    Stock,
    Sortie,
    Product,
    Facility,
    Stock,
    ProductsTranferReport,
    ProductsReceptionReport,
    StockOutReport,
    StockReport,
    ProductStockReport,
    Temporary,
    FacilityType,
    FacilityTypeProduct,
)
from import_export import resources
from import_export.admin import ExportMixin, ImportExportModelAdmin
from import_export import fields
from bdiadmin.models import CDS, District


class ProductAdminResource(resources.ModelResource):
    class Meta:
        model = Product
        fields = (
            "designation",
            "general_measuring_unit",
            "dose_par_semaine",
            "quantite_en_stock_central",
        )


class ProductAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = ProductAdminResource
    list_display = (
        "designation",
        "general_measuring_unit",
        "dose_par_semaine",
        "quantite_en_stock_central",
    )
    search_fields = ("designation", "general_measuring_unit")
    list_filter = ("dose_par_semaine",)


class FacilityAdminResource(resources.ModelResource):
    class Meta:
        model = Facility
        fields = ("id_facility", "name", "facility_level__name")


class FacilityAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = FacilityAdminResource
    list_display = (
        "id_facility",
        "name",
        "facility_level",
        "functional",
        "cds",
        "district",
        "province",
    )
    search_fields = ("id_facility", "name")
    list_filter = ("facility_level", "functional", "province")


class StockAdminResource(resources.ModelResource):
    class Meta:
        model = Stock
        fields = ("id_facility", "product", "quantity")


class StockAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = StockAdminResource
    list_display = ("id_facility", "product", "quantity")
    search_fields = ("id_facility", "product")
    list_filter = ("product",)


class ReporterAdminResource(resources.ModelResource):
    class Meta:
        model = Reporter
        fields = ("facility", "phone_number", "supervisor_phone_number")


class ReporterAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = ReporterAdminResource
    list_display = ("facility", "phone_number", "supervisor_phone_number")
    search_fields = ("facility", "phone_number", "supervisor_phone_number")
    list_filter = ("facility__facility_level__name",)


class ReportAdminResource(resources.ModelResource):
    centrale = fields.Field()
    province = fields.Field()
    facility_type = fields.Field()
    district = fields.Field()
    cds = fields.Field()

    class Meta:
        model = Report
        fields = (
            "cds",
            "hospital",
            "centrale",
            "district",
            "province",
            "reporting_date",
            "text",
            "category",
            "facility_type",
        )

    def dehydrate_cds(self, report):
        if report.facility.facility_level.name in ["CDS", "Hospital"]:
            return report.facility.name
        return

    def dehydrate_district(self, report):
        if report.facility.facility_level.name in ["CDS", "Hospital"]:
            return CDS.objects.get(code=report.facility.id_facility).district.name
        elif report.facility.facility_level.name in ["District"]:
            return report.facility.name
        return

    def dehydrate_facility_type(self, report):
        return report.facility.facility_level.name

    def dehydrate_province(self, report):
        if report.facility.facility_level.name in ["CDS", "Hospital"]:
            try:
                name = CDS.objects.get(
                    code=report.facility.id_facility
                ).district.province.name
            except Exception as e:
                print report.facility.id_facility, e
            else:
                return name
        elif report.facility.facility_level.name in ["District"]:
            return District.objects.get(code=report.facility.id_facility).province.name
        elif report.facility.facility_level.name in ["Province"]:
            return report.facility.name
        return

    def dehydrate_centrale(self, report):
        if report.facility.facility_level.name in ["Centrale"]:
            return "Centale"
        return "Burundi"


class ReportAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = ReportAdminResource
    list_display = ("facility", "reporting_date", "text", "category")
    date_hierarchy = "reporting_date"
    search_fields = ("facility__name", "reporting_date", "text", "category")
    list_filter = ("category", "facility__facility_level", "reporting_date")


class IncomingPatientsReportAdminResource(resources.ModelResource):
    class Meta:
        model = IncomingPatientsReport
        fields = (
            "total_debut_semaine",
            "ptb",
            "oedemes",
            "rechute",
            "readmission",
            "transfert_interne_i",
            "date_of_first_week_day",
            "report__reporting_date",
            "report__text",
            "report__category",
            "report__facility",
            "report__facility__facility_level",
        )


class IncomingPatientsReportAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = IncomingPatientsReportAdminResource
    list_display = (
        "total_debut_semaine",
        "ptb",
        "oedemes",
        "rechute",
        "readmission",
        "transfert_interne_i",
        "date_of_first_week_day",
        "facility",
        "type",
    )
    date_hierarchy = "date_of_first_week_day"
    search_fields = ("date_of_first_week_day",)
    list_filter = ("date_of_first_week_day", "report__facility__facility_level")

    def facility(self, obj):
        return obj.report.facility

    def type(self, obj):
        return obj.report.facility.facility_level


class OutgoingPatientsReportAdminResource(resources.ModelResource):
    class Meta:
        model = OutgoingPatientsReport
        fields = (
            "gueri",
            "deces",
            "abandon",
            "non_repondant",
            "transfert_interne_o",
            "date_of_first_week_day",
            "report__reporting_date",
            "report__text",
            "report__category",
            "report__facility",
            "report__facility__facility_level",
        )


class OutgoingPatientsReportAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = OutgoingPatientsReportAdminResource
    list_display = (
        "gueri",
        "deces",
        "abandon",
        "non_repondant",
        "transfert_interne_o",
        "date_of_first_week_day",
        "facility",
        "type",
    )
    date_hierarchy = "date_of_first_week_day"
    search_fields = ("date_of_first_week_day",)
    list_filter = ("date_of_first_week_day", "report__facility__facility_level")

    def facility(self, obj):
        return obj.report.facility

    def type(self, obj):
        return obj.report.facility.facility_level


class TransfertAdminRessource(resources.ModelResource):
    class Meta:
        model = ProductsTranferReport
        fields = (
            "sortie",
            "produit",
            "quantite_donnee",
            "sortie__destination",
            "sortie__date_de_sortie",
        )


class TransfertProductAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = TransfertAdminRessource
    list_display = ("sortie", "produit", "quantite_donnee")
    search_fields = ("produit",)
    list_filter = ("sortie__report__facility__facility_level", "sortie__date_de_sortie")


class ReceptionAdminRessource(resources.ModelResource):
    class Meta:
        model = ProductsReceptionReport
        fields = ("reception", "produit", "quantite_recue")


class ReceptionProductAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = ReceptionAdminRessource
    list_display = ("reception", "produit", "quantite_recue", "facility")
    search_fields = (
        "reception__date_de_reception",
        "reception__report__facility__name",
    )
    list_filter = ("reception__date_de_reception",)

    def facility(self, obj):
        return obj.reception.report.facility


class PatientReportsAdminRessource(resources.ModelResource):
    class Meta:
        model = PatientReports
        fields = (
            "week",
            "date_of_first_week_day",
            "facility",
            "gueri",
            "deces",
            "abandon",
            "non_repondant",
            "transfert_interne_o",
            "total_debut_semaine",
            "ptb",
            "oedemes",
            "rechute",
            "readmission",
            "transfert_interne_i",
        )


class PatientReportsAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = PatientReportsAdminRessource
    list_display = (
        "week",
        "facility",
        "total_debut_semaine",
        "ptb",
        "oedemes",
        "rechute",
        "readmission",
        "transfert_interne_i",
        "gueri",
        "deces",
        "abandon",
        "non_repondant",
        "transfert_interne_o",
    )
    date_hierarchy = "date_of_first_week_day"
    search_fields = ("facility__name",)
    list_filter = ("facility__facility_level", "week")


class ProductStockReportAdminRessource(resources.ModelResource):
    class Meta:
        model = ProductStockReport
        fields = ("stock_report", "proproductduit", "quantite_en_stock")


class ProductStockReportAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = ProductStockReportAdminRessource
    list_display = ("stock_report", "product", "quantite_en_stock")
    search_fields = ("stock_report",)
    list_filter = ("product",)


class SortieAdminRessource(resources.ModelResource):
    class Meta:
        model = Sortie
        fields = ("report__text", "date_de_sortie", "destination__id_facility")


class SortieAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = SortieAdminRessource
    list_display = ("report", "date_de_sortie", "destination")
    search_fields = ("report",)
    list_filter = ("destination",)
    date_hierarchy = "date_de_sortie"


admin.site.register(Product, ProductAdmin)
admin.site.register(Facility, FacilityAdmin)
admin.site.register(Stock, StockAdmin)
admin.site.register(Reporter, ReporterAdmin)
admin.site.register(Report, ReportAdmin)
admin.site.register(Sortie, SortieAdmin)
admin.site.register(Reception)
admin.site.register(StockOutReport)
admin.site.register(ProductsReceptionReport, ReceptionProductAdmin)
admin.site.register(ProductsTranferReport, TransfertProductAdmin)
admin.site.register(IncomingPatientsReport, IncomingPatientsReportAdmin)
admin.site.register(OutgoingPatientsReport, OutgoingPatientsReportAdmin)
admin.site.register(StockReport)
admin.site.register(ProductStockReport, ProductStockReportAdmin)
admin.site.register(Temporary)
admin.site.register(FacilityType)
admin.site.register(FacilityTypeProduct)
admin.site.register(PatientReports, PatientReportsAdmin)
