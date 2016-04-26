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
        fields = ('user', 'telephone')

class ProfileUserAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = ProfileUserResource
    search_fields = ('user', 'telephone')
    list_display = ('name', 'email', 'telephone')

    def name(self, obj):
        return obj.user.name

    def email(self, obj):
        return obj.user.email

admin.site.register(Province, ProvinceAdmin)
admin.site.register(Commune, CommuneAdmin)
admin.site.register(Colline, CollineAdmin)
admin.site.register(ProfileUser, ProfileUserAdmin)