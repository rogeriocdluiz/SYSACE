# -*- coding: utf-8 -*-
import django_tables2 as tables
from ace.models import *

from django_tables2.utils import A  # alias for Accessor

class HostTable(tables.Table):
  
    name = tables.LinkColumn('hostdetail', args=[A('pk')])
    sector = tables.Column(accessor='place.sector')
    #ip = tables.Column(accessor='ip.address')
    acoes = tables.TemplateColumn(
    	'<a class="btn btn-success btn-sm" href="/ace/host/{{record.id}}" title="visualizar" alt="visualizar"><i class="fa fa-search fa-fw"></i></a> <a class="btn btn-info btn-sm" href="/ace/host/{{record.id}}/edit" title="editar" alt="editar"><i class="fa fa-edit fa-fw"></i></a> <a class="btn btn-danger btn-sm" href="/ace/hostdel/{{record.id}}" title="excluir" alt="excluir"><i class="fa fa-trash fa-fw"></i></a>',
    	verbose_name=u'Ações',
    	orderable=False,
        exclude_from_export=True
    	)

    class Meta:
        model = Host
        template = 'django_tables2/bootstrap.html'
        attrs = {"class": "table table-striped table-advance table-hover"}
        exclude = (
        	'id',
            'supplierhw',
            'osplatform',
            'device_ptr',
            'cpu',
            'mem',
            'modification_date',
            'admuser',
            'admpass',
            'groups',
            'url',
            'vm',
            'devicemodel',
            'changed_by',
        	 )
        sequence = ('name','active','ownerid','serial_number','os','manufactorer','place','sector','hwtype','comments' )
        export_name = 'host'
        export_formats = ('csv','xls', 'xlsx','ods')


class PrinterTable(tables.Table):

    name = tables.LinkColumn('printerdetail', args=[A('pk')])
    sector = tables.Column(accessor='place.sector')
    acoes = tables.TemplateColumn(
        '<a class="btn btn-success btn-sm" href="/ace/printer/{{record.id}}" title="visualizar" alt="visualizar"><i class="fa fa-search fa-fw"></i></a> <a class="btn btn-info btn-sm" href="/ace/printer/{{record.id}}/edit" title="editar" alt="editar"><i class="fa fa-edit fa-fw"></i></a> <a class="btn btn-danger btn-sm" href="/ace/printerdel/{{record.id}}" title="excluir" alt="excluir"><i class="fa fa-trash fa-fw"></i></a>',
        verbose_name=u'Ações',
        orderable=False,
        exclude_from_export=True
    )

    class Meta:
        model = Printer
        template = 'django_tables2/bootstrap.html'
        attrs = {"class": "table table-striped table-advance table-hover"}
        exclude = (
            'id',
            'supplierhw',
            'osplatform',
            'device_ptr',
            'cpu',
            'mem',
            'modification_date',
            'admuser',
            'admpass',
            'groups',
            'url',
            'vm',
            'devicemodel',
            'os',
            'hwtype',
            'changed_by',
        )
        sequence = ('name','active', 'ownerid','serial_number', 'printer_type', 'manufactorer','place','sector', 'comments')
        export_name = 'printer'
        export_formats = ('csv', 'xls', 'xlsx', 'ods')


class ServiceTable(tables.Table):
    
    name = tables.LinkColumn('servicedetail', args=[A('pk')])
    acoes = tables.TemplateColumn(
        '<a class="btn btn-success btn-sm" href="/ace/service/{{record.id}}" title="visualizar" alt="visualizar"><i class="fa fa-search fa-fw"></i></a> <a class="btn btn-info btn-sm" href="/ace/service/{{record.id}}/edit" title="editar" alt="editar"><i class="fa fa-edit fa-fw"></i></a> <a class="btn btn-danger btn-sm" href="/ace/servicedel/{{record.id}}" title="excluir" alt="excluir"><i class="fa fa-trash fa-fw"></i></a>',
        verbose_name=u'Ações',
        orderable=False,
        exclude_from_export=True
    )

    class Meta:
        model = Service
        template = 'django_tables2/bootstrap.html'
        attrs = {"class": "table table-striped table-advance table-hover"}
        exclude = (
            'id',

        )
        #sequence = ('name', 'ownerid', 'printer_type', 'manufactorer', 'place')
        #export_name = 'service'
        #export_formats = ('csv', 'xls', 'xlsx', 'ods')


class PlaceTable(tables.Table):

    name = tables.LinkColumn('placedetail', args=[A('pk')])
    acoes = tables.TemplateColumn(
        '<a class="btn btn-success btn-sm" href="/ace/place/{{record.id}}" title="visualizar" alt="visualizar"><i class="fa fa-search fa-fw"></i></a> <a class="btn btn-info btn-sm" href="/ace/place/{{record.id}}/edit" title="editar" alt="editar"><i class="fa fa-edit fa-fw"></i></a> <a class="btn btn-danger btn-sm" href="/ace/placedel/{{record.id}}" title="excluir" alt="excluir"><i class="fa fa-trash fa-fw"></i></a>',
        verbose_name=u'Ações',
        orderable=False,
        exclude_from_export=True
    )

    class Meta:
        model = Place
        template = 'django_tables2/bootstrap.html'
        attrs = {"class": "table table-striped table-advance table-hover"}
        exclude = (
            'id',

        )
        #sequence = ('name', 'ownerid', 'printer_type', 'manufactorer', 'place')
        #export_name = 'service'
        #export_formats = ('csv', 'xls', 'xlsx', 'ods')



class SectorTable(tables.Table):

    name = tables.LinkColumn('sectordetail', args=[A('pk')])        
    acoes = tables.TemplateColumn(
        '<a class="btn btn-success btn-sm" href="/ace/sector/{{record.id}}" title="visualizar" alt="visualizar"><i class="fa fa-search fa-fw"></i></a> <a class="btn btn-info btn-sm" href="/ace/sector/{{record.id}}/edit" title="editar" alt="editar"><i class="fa fa-edit fa-fw"></i></a> <a class="btn btn-danger btn-sm" href="/ace/sectordel/{{record.id}}" title="excluir" alt="excluir"><i class="fa fa-trash fa-fw"></i></a>',
        verbose_name=u'Ações',
        orderable=False,
        exclude_from_export=True
    )

    class Meta:
        model = Sector
        template = 'django_tables2/bootstrap.html'
        attrs = {"class": "table table-striped table-advance table-hover"}
        exclude = (
            'id',

        )
        #sequence = ('name', 'ownerid', 'printer_type', 'manufactorer', 'place')
        #export_name = 'service'
        #export_formats = ('csv', 'xls', 'xlsx', 'ods')




class NetpointTable(tables.Table):

    num = tables.LinkColumn('pointdetail', args=[A('pk')])
    acoes = tables.TemplateColumn(
        '<a class="btn btn-success btn-sm" href="/ace/point/{{record.id}}" title="visualizar" alt="visualizar"><i class="fa fa-search fa-fw"></i></a> <a class="btn btn-info btn-sm" href="/ace/netpoint/{{record.id}}/edit" title="editar" alt="editar"><i class="fa fa-edit fa-fw"></i></a> <a class="btn btn-danger btn-sm" href="/ace/netpointdel/{{record.id}}" title="excluir" alt="excluir"><i class="fa fa-trash fa-fw"></i></a>',
        verbose_name=u'Ações',
        orderable=False,
        exclude_from_export=True
    )

    class Meta:
        model = Netpoint
        template = 'django_tables2/bootstrap.html'
        attrs = {"class": "table table-striped table-advance table-hover"}
        exclude = (
            'id',
            'modification_date',
            'creation_date',
            'comments',
            'patchpanel',
            'patchpanelport',
            'switch',
            'swport',
            'phone',
        )
        #   sequence = ('name', 'ownerid', 'printer_type', 'manufactorer', 'place')
        export_name = 'netpoint'
        export_formats = ('csv', 'xls', 'xlsx', 'ods')



class IpTable(tables.Table):

    address = tables.LinkColumn('ipdetail', args=[A('pk')])
    acoes = tables.TemplateColumn(
        '<a class="btn btn-success btn-sm" href="/ace/ip/{{record.id}}" title="visualizar" alt="visualizar"><i class="fa fa-search fa-fw"></i></a> <a class="btn btn-info btn-sm" href="/ace/ip/{{record.id}}/edit" title="editar" alt="editar"><i class="fa fa-edit fa-fw"></i></a> <a class="btn btn-danger btn-sm" href="/ace/ipdel/{{record.id}}" title="excluir" alt="excluir"><i class="fa fa-trash fa-fw"></i></a>',
        verbose_name=u'Ações',
        orderable=False,
        exclude_from_export=True
    )

    class Meta:
        model = Ip
        template = 'django_tables2/bootstrap.html'
        attrs = {"class": "table table-striped table-advance table-hover"}
        exclude = (
            'id',
            'modification_date',
            'comments',

        )
        #sequence = ('name', 'ownerid', 'printer_type', 'manufactorer', 'place')
        export_name = 'ip'
        export_formats = ('csv', 'xls', 'xlsx', 'ods')


class RackTable(tables.Table):

    name = tables.LinkColumn('rackdetail', args=[A('pk')])    
    acoes = tables.TemplateColumn(
        '<a class="btn btn-success btn-sm" href="/ace/rack/{{record.id}}" title="visualizar" alt="visualizar"><i class="fa fa-search fa-fw"></i></a> <a class="btn btn-info btn-sm" href="/ace/rack/{{record.id}}/edit" title="editar" alt="editar"><i class="fa fa-edit fa-fw"></i></a> <a class="btn btn-danger btn-sm" href="/ace/rackdel/{{record.id}}" title="excluir" alt="excluir"><i class="fa fa-trash fa-fw"></i></a>',
        verbose_name=u'Ações',
        orderable=False,
        exclude_from_export=True
    )

    class Meta:
        model = Rack
        template = 'django_tables2/bootstrap.html'
        attrs = {"class": "table table-striped table-advance table-hover"}
        exclude = (
            'id',
            'comments',
        )
        #sequence = ('name', 'ownerid', 'printer_type', 'manufactorer', 'place')
        export_name = 'rack'
        export_formats = ('csv', 'xls', 'xlsx', 'ods')



class PatchpanelTable(tables.Table):

    num = tables.LinkColumn('patchpaneldetail', args=[A('pk')])
    acoes = tables.TemplateColumn(
        '<a class="btn btn-success btn-sm" href="/ace/patchpanel/{{record.id}}" title="visualizar" alt="visualizar"><i class="fa fa-search fa-fw"></i></a> <a class="btn btn-info btn-sm" href="/ace/patchpanel/{{record.id}}/edit" title="editar" alt="editar"><i class="fa fa-edit fa-fw"></i></a> <a class="btn btn-danger btn-sm" href="/ace/patchpaneldel/{{record.id}}" title="excluir" alt="excluir"><i class="fa fa-trash fa-fw"></i></a>',
        verbose_name=u'Ações',
        orderable=False,
        exclude_from_export=True
    )

    class Meta:
        model = Patchpanel
        template = 'django_tables2/bootstrap.html'
        attrs = {"class": "table table-striped table-advance table-hover"}
        exclude = (
            'id',
            'comments',
        )
        #sequence = ('name', 'ownerid', 'printer_type', 'manufactorer', 'place')
        export_name = 'patchpanel'
        export_formats = ('csv', 'xls', 'xlsx', 'ods')



class NetworkTable(tables.Table):

    name = tables.LinkColumn('networkdetail', args=[A('pk')])
    acoes = tables.TemplateColumn(
        '<a class="btn btn-success btn-sm" href="/ace/network/{{record.id}}" title="visualizar" alt="visualizar"><i class="fa fa-search fa-fw"></i></a> <a class="btn btn-info btn-sm" href="/ace/network/{{record.id}}/edit" title="editar" alt="editar"><i class="fa fa-edit fa-fw"></i></a> <a class="btn btn-danger btn-sm" href="/ace/networkdel/{{record.id}}" title="excluir" alt="excluir"><i class="fa fa-trash fa-fw"></i></a>',
        verbose_name=u'Ações',
        orderable=False,
        exclude_from_export=True
    )

    class Meta:
        model = Network
        template = 'django_tables2/bootstrap.html'
        attrs = {"class": "table table-striped table-advance table-hover"}
        exclude = (
            'id',
            'comments',
            'dhcp_start',
            'dhcp_end',
            'gateway',
            'mask'
        )
        #sequence = ('name', 'ownerid', 'printer_type', 'manufactorer', 'place')
        export_name = 'network'
        export_formats = ('csv', 'xls', 'xlsx', 'ods')


class StackTable(tables.Table):

    name = tables.LinkColumn('stackdetail', args=[A('pk')])
    acoes = tables.TemplateColumn(
        '<a class="btn btn-success btn-sm" href="/ace/stack/{{record.id}}" title="visualizar" alt="visualizar"><i class="fa fa-search fa-fw"></i></a> <a class="btn btn-info btn-sm" href="/ace/stack/{{record.id}}/edit" title="editar" alt="editar"><i class="fa fa-edit fa-fw"></i></a> <a class="btn btn-danger btn-sm" href="/ace/stackdel/{{record.id}}" title="excluir" alt="excluir"><i class="fa fa-trash fa-fw"></i></a>',
        verbose_name=u'Ações',
        orderable=False,
        exclude_from_export=True
    )

    class Meta:
        model = Stack
        template = 'django_tables2/bootstrap.html'
        attrs = {"class": "table table-striped table-advance table-hover"}
        exclude = (
            'id',
            'active',
            'ownerid',
            'devicemodel',
            'admuser',
            'admpass',
            'modification_date',
            'device_ptr'
            
        )
        #sequence = ('name', 'ownerid', 'printer_type', 'manufactorer', 'place')
        export_name = 'stack'
        export_formats = ('csv', 'xls', 'xlsx', 'ods')        


class SwitchTable(tables.Table):

    name = tables.LinkColumn('switchdetail', args=[A('pk')])
    acoes = tables.TemplateColumn(
        '<a class="btn btn-success btn-sm" href="/ace/switch/{{record.id}}" title="visualizar" alt="visualizar"><i class="fa fa-search fa-fw"></i></a> <a class="btn btn-info btn-sm" href="/ace/switch/{{record.id}}/edit" title="editar" alt="editar"><i class="fa fa-edit fa-fw"></i></a> <a class="btn btn-danger btn-sm" href="/ace/switchdel/{{record.id}}" title="excluir" alt="excluir"><i class="fa fa-trash fa-fw"></i></a>',
        verbose_name=u'Ações',
        orderable=False,
        exclude_from_export=True
    )

    class Meta:
        model = Switch
        template = 'django_tables2/bootstrap.html'
        attrs = {"class": "table table-striped table-advance table-hover"}
        exclude = (
            'id',
            'comments',
            'url',
            'admuser',
            'admpass',
            'device_ptr',
            'serial',
            'ports',
            'stacked',
            'snmpcom',
            'changed_by',
            'stack_field',
            'snmp',
            'rack',
            'modification_date',
            'manageable',
            'place',
            'model',
            'snmp'
        )
        #sequence = ('name', 'ownerid', 'printer_type', 'manufactorer', 'place')
        export_name = 'switch'
        export_formats = ('csv', 'xls', 'xlsx', 'ods')        


class VlanTable(tables.Table):

    vlanid = tables.LinkColumn('vlandetail', args=[A('pk')])
    acoes = tables.TemplateColumn(
        '<a class="btn btn-success btn-sm" href="/ace/vlan/{{record.id}}" title="visualizar" alt="visualizar"><i class="fa fa-search fa-fw"></i></a> <a class="btn btn-info btn-sm" href="/ace/vlan/{{record.id}}/edit" title="editar" alt="editar"><i class="fa fa-edit fa-fw"></i></a> <a class="btn btn-danger btn-sm" href="/ace/vlandel/{{record.id}}" title="excluir" alt="excluir"><i class="fa fa-trash fa-fw"></i></a>',
        verbose_name=u'Ações',
        orderable=False,
        exclude_from_export=True
    )

    class Meta:
        model = Vlan
        template = 'django_tables2/bootstrap.html'
        attrs = {"class": "table table-striped table-advance table-hover"}
        exclude = (
            'id',
      
        )


class PhoneTable(tables.Table):

    num = tables.LinkColumn('phonedetail', args=[A('pk')])
    acoes = tables.TemplateColumn(
        '<a class="btn btn-success btn-sm" href="/ace/phone/{{record.id}}" title="visualizar" alt="visualizar"><i class="fa fa-search fa-fw"></i></a> <a class="btn btn-info btn-sm" href="/ace/phone/{{record.id}}/edit" title="editar" alt="editar"><i class="fa fa-edit fa-fw"></i></a> <a class="btn btn-danger btn-sm" href="/ace/phonedel/{{record.id}}" title="excluir" alt="excluir"><i class="fa fa-trash fa-fw"></i></a>',
        verbose_name=u'Ações',
        orderable=False,
        exclude_from_export=True
    )


    class Meta:
        model = Phone
        template = 'django_tables2/bootstrap.html'
        attrs = {"class": "table table-striped table-advance table-hover"}
        exclude = (
            'id',
            'date_creation',
            'date_modification',
            'newpassword',
            'dist',
            'bloco',
            'par',
            'dg',
            'changed_by',
            'password'
        )
        #sequence = ('num', 'active','user', 'place', 'phonecategory','telephonetype','phonehw',)
        export_name = 'phone'
        export_formats = ('csv', 'xls', 'xlsx', 'ods')          


class PasswordTable(tables.Table):

    user = tables.LinkColumn('phonedetail', args=[A('pk')])
    acoes = tables.TemplateColumn(
        '<a class="btn btn-success btn-sm" href="/ace/phone/{{record.id}}" title="visualizar" alt="visualizar"><i class="fa fa-search fa-fw"></i></a> <a class="btn btn-info btn-sm" href="/ace/phone/{{record.id}}/edit" title="editar" alt="editar"><i class="fa fa-edit fa-fw"></i></a> <a class="btn btn-danger btn-sm" href="/ace/phonedel/{{record.id}}" title="excluir" alt="excluir"><i class="fa fa-trash fa-fw"></i></a>',
        verbose_name=u'Ações',
        orderable=False,
        exclude_from_export=True
    )

    class Meta:
        model = Phone
        template = 'django_tables2/bootstrap.html'
        attrs = {"class": "table table-striped table-advance table-hover"}
        exclude = (
            'id',
            'date_creation',
            'date_modification',
            'newpassword',
            'dist',
            'bloco',
            'par',
            'dg',
            'changed_by',
            'phonehw',
            'telephonetype',
            'num',
            'place',
            'password'
        )
        sequence = ('user', 'active',  'phonecategory',)
        export_name = 'phone'
        export_formats = ('csv', 'xls', 'xlsx', 'ods')            


class UserTable(tables.Table):

    username = tables.LinkColumn('userdetail', args=[A('pk')])
    acoes = tables.TemplateColumn(
        '<a class="btn btn-success btn-sm" href="/ace/user/{{record.id}}" title="visualizar" alt="visualizar"><i class="fa fa-search fa-fw"></i></a> <a class="btn btn-info btn-sm" href="/ace/user/{{record.id}}/edit" title="editar" alt="editar"><i class="fa fa-edit fa-fw"></i></a> ',
        verbose_name=u'Ações',
        orderable=False,
        exclude_from_export=True
    )

    class Meta:
        model = User
        template = 'django_tables2/bootstrap.html'
        attrs = {"class": "table table-striped table-advance table-hover"}
        exclude = (
            'id',
            'password',
            'is_superuser',
            'is_staff',
            'is_active',
            'date_joined',
            'last_login',
        )
        #sequence = ('firstname', 'lastname','email')
        export_name = 'user'
        export_formats = ('csv', 'xls', 'xlsx', 'ods')



class PhoneAssociationTable(tables.Table):

    #phone = tables.LinkColumn('phonedetail', args=[A('pk')])
    #user = tables.LinkColumn('userdetail', text=lambda record: record, args=[A('record.user.pk')])
    #password = tables.Column(accessor='phone.password')
    acoes = tables.TemplateColumn(
        '<a class="btn btn-success btn-sm" href="/ace/phone/{{record.phone.id}}" title="visualizar" alt="visualizar"><i class="fa fa-search fa-fw"></i></a> ',
        verbose_name=u'Ações',
        orderable=False,
        exclude_from_export=True
    )

    class Meta:
        model = Phoneownership
        template = 'django_tables2/bootstrap.html'
        attrs = {"class": "table table-striped table-advance table-hover"}
        exclude = (
            'id',
        )
        export_name = 'phone'
        export_formats = ('csv', 'xls', 'xlsx', 'ods')
        sequence = ('active', 'phone', 'user', 'date_activation', 'date_deactivation')


class PasswordAssociationTable(tables.Table):

    acoes = tables.TemplateColumn(
        '<a class="btn btn-success btn-sm" href="/ace/phone/{{record.phone.id}}" title="visualizar" alt="visualizar"><i class="fa fa-search fa-fw"></i></a> ',
        verbose_name=u'Ações',
        orderable=False,
        exclude_from_export=True
    )

    class Meta:
        model = Phoneownership
        template = 'django_tables2/bootstrap.html'
        attrs = {"class": "table table-striped table-advance table-hover"}
        exclude = (
            'id',
            'phone',
        )
        export_name = 'phone'
        export_formats = ('csv', 'xls', 'xlsx', 'ods')
        sequence = ('active','phone', 'user', 'date_activation', 'date_deactivation')