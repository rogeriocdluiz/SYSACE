# -*- coding: utf-8 -*-

from django.contrib import admin

from django.contrib.admin.options import ModelAdmin, TabularInline
#from ace.models import Place, Switch, Netpoint, Rack, Switchport, Floor, Manufactorer, Patchpanel, Patchpanelport, Phonecategory, Phonetype, Phone, Network, Ip, Device, Stack, Host, Hosttype, Os , Servicecategory, Service, Device, Ownerid, Sector, Printer, Devicemodel, Phoneownership
from ace.models import *

from django.contrib.admin import AdminSite

from simple_history.admin import SimpleHistoryAdmin


#django-import-export
from import_export import resources

from import_export.admin import ImportExportModelAdmin

from .forms import HostForm, ServiceForm, SwitchForm,NetpointForm




AdminSite.site_header = 'Administração de sistemas'

#solo
from solo.admin import SingletonModelAdmin
from ace.models import AceConfig

admin.site.register(AceConfig, SingletonModelAdmin)



#exportação CSV
def export_csv(modeladmin, request, queryset):
    import csv
    from django.utils.encoding import smart_str
    from django.http import HttpResponseRedirect, HttpResponse
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=netpoint.csv'
    writer = csv.writer(response, csv.excel)
    response.write(u'\ufeff'.encode('utf8')) # BOM (optional...Excel needs it to open UTF-8 file properly)
    writer.writerow([
        smart_str(u"Num"),
        smart_str(u"Tipo"),
        smart_str(u"Local"),
        smart_str(u"Rack"),
        smart_str(u"Phone"),
        smart_str(u"Switch"),
        smart_str(u"Porta_Switch"),
    ])
    for obj in queryset:
        writer.writerow([
            smart_str(obj.num),
			smart_str(obj.pointtype),            
            smart_str(obj.place),
            smart_str(obj.rack),
            smart_str(obj.phone),
            smart_str(obj.switch),
            smart_str(obj.swport),
        ])
    return response
export_csv.short_description = u"Exportar em CSV"



#importacao e exportacao
class HostResource(resources.ModelResource):

    class Meta:
        model = Host


class PrinterResource(resources.ModelResource):

    class Meta:
        model = Printer






class StackAdmin(admin.ModelAdmin):
    list_display = ('name', 'url')
    list_filter = ('name',)
    exclude=("ownerid","devicemodel")
    readonly_fields=('ownerid','devicemodel' )

	#def get_readonly_fields(self, request, obj=None):
	#    if obj: # editing an existing object
	#        return self.readonly_fields + ('ownerid')
	#    return self.readonly_fields




class SwitchportInline(admin.TabularInline):
    model = Switchport
    extra = 3


class SwitchAdmin(admin.ModelAdmin):

	inlines = [SwitchportInline]
	list_display = ('name', 'model', 'manufactorer', 'place','rack' ,'ports','url','serial','stacked','ports_total',)
	list_filter = ('manufactorer','model','place')
	form = SwitchForm





class NetpointAdmin(admin.ModelAdmin):
    list_display = ('num', 'place','rack', 'patchpanel', 'patchpanelport','pointtype','switch','swport','modification_date','creation_date')
    list_filter = ( 'place','pointtype')
    search_fields = ['num']
    actions = [export_csv]

    fieldsets = (
	    (None, {
    	    'fields': ('num', 'pointtype','place','rack','patchpanel','patchpanelport', 'switch', 'swport', 'comments')
    	}),
    	('Informações de pontos de voz', {
            'classes': ('grp-collapse grp-open',),           
            'fields': ('phone', 'dist', 'bloco', 'par', 'dg')
        }),
        )
    form = NetpointForm


class SwitchportAdmin(admin.ModelAdmin):
	list_display = ('num', 'switch','tipo','obs')
	list_filter = ('switch','vlans')
	search_fields = ['num']


class NetpointInline(admin.TabularInline):
    model = Netpoint
    extra = 3


class PlaceAdmin(admin.ModelAdmin):

	list_display = ('name', 'floor', 'placetype', 'comments')
	search_fields = ['name']


class VlanAdmin(admin.ModelAdmin):

    list_display = ('name', 'comments')
    search_fields = ['name']



class PatchpanelInline(admin.TabularInline):
    model = Patchpanel
    extra = 3


class RackAdmin(admin.ModelAdmin):
	inlines = [PatchpanelInline]
	list_display = ('name', 'place','patchpanel_total')


class PatchpanelportAdmin(admin.ModelAdmin):
    list_display = ('num', 'patchpanel')



class PatchpanelportInline(admin.TabularInline):
    model = Patchpanelport
    extra = 3



class PatchpanelAdmin(admin.ModelAdmin):
	inlines = [PatchpanelportInline,]
	list_display = ('num', 'rack')
	list_filter = ('rack',)



class PhoneAdmin(SimpleHistoryAdmin,ImportExportModelAdmin):
	list_display = ('num', 'user','telephonetype','phonecategory','place','active','password','newpassword')
	list_filter = ('active','telephonetype','phonecategory','password','newpassword','place')
	search_fields = ['num']

class PhonecategoryAdmin(admin.ModelAdmin):
	list_display = ('num', 'name')
	search_fields = ['num', 'name']	


class PhonetypeAdmin(admin.ModelAdmin):
	list_display = ('name',)
	search_fields = ['name',]		


class NetworkAdmin(admin.ModelAdmin):
	list_display = ('name','address','dhcp','mask' )
	list_filter = ('dhcp','vln')


class IpAdmin(admin.ModelAdmin):
	list_display = ('address','network' )
	list_filter = ('network',)	

class ServicecategoryAdmin(admin.ModelAdmin):
	list_display = ('name', )

class ServiceAdmin(admin.ModelAdmin):
	list_display = ('name','ip' )
	form = ServiceForm
	#list_filter = ('host',)	

class SectorAdmin(admin.ModelAdmin):
	list_display = ('name', )


class HostupdateInline(admin.TabularInline):
    model = Hostupdate
    extra = 3



class HostAdmin(ImportExportModelAdmin):
    list_display = ('name', 'hwtype','vm' ,'os')
    list_filter = ('hwtype','vm','active','devicemodel','manufactorer')
    inlines = [HostupdateInline]
    search_fields = ['name',]	
    form = HostForm
    pass   

class PrinterAdmin(ImportExportModelAdmin):
	list_display = ('name', 'model', 'place')
	list_filter = ('model','place','manufactorer',)
	search_fields = ['name',]	
	#form = PrinterForm
    #	pass   




class HosttypeAdmin(admin.ModelAdmin):
	list_display = ('name',)
	

class OsAdmin(admin.ModelAdmin):
	list_display = ('name', 'version')

class OwneridAdmin(admin.ModelAdmin):
	list_display = ('num',)	


class PhoneownershipAdmin(ImportExportModelAdmin)    :
    list_display = ('user','phone', 'date_activation', 'date_deactivation')


    
	
#class PhonetypeAdmin(admin.ModelAdmin):
#	list_display = ('name',)	
		

admin.site.register(Place, PlaceAdmin)
admin.site.register(Stack, StackAdmin)
admin.site.register(Switch, SwitchAdmin)
admin.site.register(Netpoint, NetpointAdmin)
admin.site.register(Rack, RackAdmin)
admin.site.register(Switchport, SwitchportAdmin)
admin.site.register(Floor)
admin.site.register(Vlan)
admin.site.register(Manufactorer)
admin.site.register(Patchpanel, PatchpanelAdmin)
admin.site.register(Patchpanelport,PatchpanelportAdmin)
admin.site.register(Phone, PhoneAdmin)
admin.site.register(Network, NetworkAdmin)
admin.site.register(Ip, IpAdmin)
admin.site.register(Os, OsAdmin)
admin.site.register(Host, HostAdmin)
admin.site.register(Printer, PrinterAdmin)
admin.site.register(Hosttype, HosttypeAdmin)
admin.site.register(Servicecategory, ServicecategoryAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Sector, SectorAdmin)
admin.site.register(Ownerid, OwneridAdmin)
admin.site.register(Phonecategory, PhonecategoryAdmin)
admin.site.register(Phonetype, PhonetypeAdmin)
admin.site.register(Devicemodel)
admin.site.register(Hostupdate)
#admin.site.register(Phoneownership, PhoneownershipAdmin)





