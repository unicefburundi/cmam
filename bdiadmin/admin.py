from django.contrib import admin
from import_export import resources
from import_export.admin import ExportMixin
from bdiadmin.models import *


class ProvinceResource(resources.ModelResource):
    class Meta:
        model = Province
        fields = ('name', 'code')


class ProvinceAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = ProvinceResource
    search_fields = ('name', 'code')
    list_display = ('name', 'code')


class CommuneResource(resources.ModelResource):
    class Meta:
        model = Commune
        fields = ('name', 'code', 'province__name')


class CommuneAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = CommuneResource
    search_fields = ('name', 'code')
    list_display = ('name', 'code', 'province')
    list_filter = ('province__name',)


class CollineResource(resources.ModelResource):
    class Meta:
        model = Colline
        fields = ('name', 'code', 'commune__name', 'commune__province__name')


class CollineAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = CollineResource
    search_fields = ('name', 'code')
    list_display = ('name', 'code', 'commune', 'province')
    list_filter = ('commune__province__name',)

    def province(self, obj):
        return obj.commune.province.name


class ProfileUserResource(resources.ModelResource):
    class Meta:
        model = ProfileUser
        fields = ('user__email', 'telephone', 'level', 'user__username')


class ProfileUserAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = ProfileUserResource
    search_fields = ('user', 'telephone', 'level')
    list_display = ('name', 'email', 'telephone', 'level')

    def name(self, obj):
        return obj.user.username

    def email(self, obj):
        return obj.user.email


class DistrictResource(resources.ModelResource):
    class Meta:
        model = District
        fields = ('name', 'code', 'province')


class DistrictAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = DistrictResource
    search_fields = ('name', 'code')
    list_display = ('name', 'code', 'province')
    list_filter = ('province',)


class CDSResource(resources.ModelResource):
    class Meta:
        model = CDS
        fields = ('name', 'code', 'district', 'district__province__name')


class CDSAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = CDSResource
    search_fields = ('name', 'code')
    list_display = ('name', 'code', 'district', 'province')
    list_filter = ('district__province', 'district', )

    def province(self, obj):
        return obj.district.province

admin.site.register(Province, ProvinceAdmin)
admin.site.register(Commune, CommuneAdmin)
admin.site.register(Colline, CollineAdmin)
admin.site.register(ProfileUser, ProfileUserAdmin)
admin.site.register(District, DistrictAdmin)
admin.site.register(CDS, CDSAdmin)
