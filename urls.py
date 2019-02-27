from django.conf.urls import url, include, handler400
from ace import views

#from ace.views import OwneridAutocomplete, OsAutocomplete, HosttypeAutocomplete, ManufactorerAutocomplete, PlaceAutocomplete, StackAutocomplete, IpAutocomplete, NetworkAutocomplete, HostAutocomplete, DeviceAutocomplete, ServicecategoryAutocomplete, SwitchAutocomplete, SwitchportAutocomplete, SwitchrackAutocomplete, PatchpanelAutocomplete, PatchpanelportAutocomplete, PhoneAutocomplete, RackAutocomplete, UserAutocomplete

#from ace.views import PlaceCreateModal, IpCreateModal, ServiceCreateModal, ServiceCategoryCreateModal, FloorCreateModal, UserCreateModal, OwneridCreateModal, ManufactorerCreateModal, RackCreateModal, StackCreateModal,  SwitchCreateModal, HostCreateModal, NetworkCreateModal, PatchpanelCreateModal, PatchpanelportCreateModal, OsCreateModal, HosttypeCreateModal, PhonecategoryCreateModal, SwitchportCreateModal, SectorCreateModal, UserCreateModal, DevicemodelCreateModal, PhoneCreateModal

from ace.views import *

from django_filters.views import FilterView

#handler403 = 'ace.views.permission_denied_view'

urlpatterns = [
	
    url(r'^$', views.index, name='ace_index'),

    url(r'^config/$', views.config, name='config'),

    url(r'^confignew/$', views.config_new, name='config_new'),

    url(r'^configedit/$', views.config_edit, name='config_edit'),

    url(r'^switchlist/$', views.switchlist, name='switchlist'),

    url(r'^stacklist/$', views.stacklist, name='stacklist'),

    url(r'^racklist/$', views.racklist, name='racklist'),

    url(r'^patchpanellist/$', views.patchpanellist, name='patchpanellist'),

    url(r'^hostlist/$', views.hostlist, name='hostlist'),

    url(r'^vlanlist/$', views.vlanlist, name='vlanlist'),

    url(r'^printerlist/$', views.printerlist, name='printerlist'),

    url(r'^servicelist/$', views.servicelist, name='servicelist'),   
    
    url(r'^iplist/$', views.iplist, name='iplist'), 

    url(r'^networklist/$', views.networklist, name='networklist'),    

    url(r'^userlist/$', views.userlist, name='userlist'),       

    url(r'^owneridlist/$', views.owneridlist, name='owneridlist'),     

    
    url(r'^places/$', views.placelist, name='placelist'),

    url(r'^sectors/$', views.sectorlist, name='sectorlist'),

    url(r'^place/(?P<place_id>\d+)/$', views.placedetail, name='placedetail'),    

    url(r'^sector/(?P<sector_id>\d+)/$', views.sectordetail, name='sectordetail'),


    url(r'^netpoints/$', views.netpointlist, name='netpointlist'),

    url(r'^phonelist/$', views.phonelist, name='phonelist'),

    url(r'^passwordlist/$', views.passwordlist, name='passwordlist'),

    url(r'^phoneassociation/$', views.phoneassociation, name='phoneassociation'),

    url(r'^passassociation/$', views.passwordassociation, name='passassociation'),

    url(r'^switch/(?P<switch_id>\d+)/$', views.switchdetail, name='switchdetail'),

    url(r'^stack/(?P<pilha_id>\d+)/$', views.stackdetail, name='stackdetail'),

    url(r'^rack/(?P<rack_id>\d+)/$', views.rackdetail, name='rackdetail'),

    url(r'^patchpanel/(?P<patchpanel_id>\d+)/$', views.patchpaneldetail, name='patchpaneldetail'),

    url(r'^vlan/(?P<vlan_id>\d+)/$', views.vlandetail, name='vlandetail'),

    url(r'^swport/(?P<portaswitch_id>\d+)/$', views.swport, name='swport'),

    url(r'^point/(?P<ponto_id>\d+)/$', views.pointdetail, name='pointdetail'),

    url(r'^host/(?P<host_id>\d+)/$', views.hostdetail, name='hostdetail'),

    url(r'^printer/(?P<printer_id>\d+)/$', views.printerdetail, name='printerdetail'),
    

    url(r'^service/(?P<service_id>\d+)/$', views.servicedetail, name='servicedetail'),

    url(r'^ip/(?P<ip_id>\d+)/$', views.ipdetail, name='ipdetail'),    

    url(r'^network/(?P<rede_id>\d+)/$', views.networkdetail, name='networkdetail'),  

    url(r'^servicecat/(?P<servicecategory_id>\d+)/$', views.servicecatdetail, name='servicecatdetail'),

    url(r'^user/(?P<user_id>\d+)/$', views.userdetail, name='userdetail'),    

    url(r'^ownerid/(?P<ownerid_id>\d+)/$', views.owneriddetail, name='owneriddetail'),

    url(r'^patchpanel/(?P<pachpanel_id>\d+)/$', views.patchpaneldetail, name='patchpaneldetail'),        

    url(r'^patchpanelport/(?P<patchpanelport_id>\d+)/$', views.patchpanelport, name='patchpanelport'),       
    


    url(r'^phone/(?P<phone_id>\d+)/$', views.phonedetail, name='phonedetail'),

    url(r'^login/$', views.user_login, name='login'),

    url(r'^logout/$', views.user_logout, name='logout'),

    
    url(r'^search/$', views.search, name='search'),


    url(r'^placereport/(?P<local_id>\d+)/$', views.placereport, name='placereport'),
    url(r'^placereportblank/$', views.placereportblank, name='placereportblank'),

    url(r'^freepointsreport/$', views.freepointsreport, name='freepointsreport'),

    url(r'^netpointsreport/$', views.netpointsreport, name='netpointsreport'),

    url(r'^switchreport/$', views.switchreport, name='switchreport'),

    url(r'^hostreport/$', views.hostreport, name='hostreport'),

    url(r'^printerreport/$', views.printerreport, name='printerreport'),    
 

    url(r'^hostdetailreport/(?P<host_id>\d+)$', views.hostdetailreport, name='hostdetailreport'),

    url(r'^servicereport/$', views.servicereport, name='servicereport'),

    url(r'^ipreport/$', views.ipreport, name='ipreport'),

    url(r'^pwreport/$', views.pwreport, name='pwreport'),

    url(r'^pwreportopen/$', views.pwreportopen, name='pwreportopen'),

    url(r'^phonereport/$', views.phonereport, name='phonereport'),

    url(r'^rackreport/(?P<rack_id>\d+)$', views.rackreport, name='rackreport'),



    url(r'^host/new/$', views.host_new, name='host_new'),

    #testes
    url(r'^host/create/$', views.host_create, name='host_create'),


    url(r'^host/(?P<pk>[0-9]+)/edit/$', views.host_edit, name='host_edit'),

    url(r'^hostdel/(?P<pk>\d+)$', views.host_delete, name='host_delete'),


    url(r'^upd/new/(?P<pk>[0-9]+)$', views.update_new, name='update_new'),

    url(r'^upd/(?P<pk>[0-9]+)/(?P<h>[0-9]+)/edit/$', views.update_edit, name='update_edit'),


    url(r'^printer/new/$', views.printer_new, name='printer_new'),

    url(r'^printer/(?P<pk>[0-9]+)/edit/$', views.printer_edit, name='printer_edit'),

    url(r'^printerdel/(?P<pk>\d+)$', views.printer_delete, name='printer_delete'),




    url(r'^service/new/$', views.service_new, name='service_new'),

    url(r'^service/(?P<pk>[0-9]+)/edit/$', views.service_edit, name='service_edit'),

    url(r'^servicedel/(?P<pk>\d+)$', views.service_delete, name='service_delete'),


    url(r'^network/new/$', views.network_new, name='network_new'),

    url(r'^network/(?P<pk>[0-9]+)/edit/$', views.network_edit, name='network_edit'),

    url(r'^networkdel/(?P<pk>\d+)$', views.network_delete, name='network_delete'),
   

    url(r'^ip/new/$', views.ip_new, name='ip_new'),
    #url(r'^ip/new/(?P<pk>\d+)/(?P<ipaddr>\d+)/$', views.ip_new, name='ip_new'),
    url(r'^ip/new/(?P<pk>\d+)/(?P<ipaddr>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})/$', views.ip_new2, name='ip_new2'),
    #url(r'^ip/new/(?P<pk>\d+)/(ipaddr=(?P<ipaddr>\d+))$', views.ip_new, name='ip_new'),


    url(r'^ip/(?P<pk>[0-9]+)/edit/$', views.ip_edit, name='ip_edit'),

    url(r'^ipdel/(?P<pk>\d+)$', views.ip_delete, name='ip_delete'),   


    url(r'^phone/new/$', views.phone_new, name='phone_new'),

    #url(r'^phone/new2/$', views.phone_new2, name='phone_new2'),

    url(r'^phone/(?P<pk>[0-9]+)/edit/$', views.phone_edit, name='phone_edit'),

    url(r'^phonedel/(?P<pk>\d+)$', views.phone_delete, name='phone_delete'),  


    #url(r'^phoneownership/new/$', views.phoneownership_new, name='phoneownership_new'),
    url(r'^phoneownership/(?P<pk>\d+)$', views.phoneownership_new, name='phoneownership_new'),

    url(r'^phoneownership/disable/(?P<pk>[0-9]+)$', views.phoneownership_disable, name='phoneownership_disable'),


    url(r'^place/new/$', views.place_new, name='place_new'),

    url(r'^place/(?P<pk>[0-9]+)/edit/$', views.place_edit, name='place_edit'),

    url(r'^placedel/(?P<pk>\d+)$', views.place_delete, name='place_delete'),  


    url(r'^sector/new/$', views.sector_new, name='sector_new'),

    url(r'^sector/(?P<pk>[0-9]+)/edit/$', views.sector_edit, name='sector_edit'),

    url(r'^sectordel/(?P<pk>\d+)$', views.sector_delete, name='sector_delete'),  

    
    url(r'^rack/new/$', views.rack_new, name='rack_new'),

    url(r'^rack/(?P<pk>[0-9]+)/edit/$', views.rack_edit, name='rack_edit'),

    url(r'^rackdel/(?P<pk>\d+)$', views.rack_delete, name='rack_delete'), 


    url(r'^patchpanel/new/$', views.patchpanel_new, name='patchpanel_new'),

    url(r'^patchpanel/(?P<pk>[0-9]+)/edit/$', views.patchpanel_edit, name='patchpanel_edit'),

    url(r'^patchpaneldel/(?P<pk>\d+)$', views.patchpanel_delete, name='patchpanel_delete'), 


    url(r'^patchpanelport/new/$', views.patchpanelport_new, name='patchpanelport_new'),

    url(r'^patchpanelport/(?P<pk>[0-9]+)/edit/$', views.patchpanelport_edit, name='patchpanelport_edit'),

    url(r'^patchpanelportdel/(?P<pk>\d+)$', views.patchpanelport_delete, name='patchpanelport_delete'),     




    url(r'^stack/new/$', views.stack_new, name='stack_new'),

    url(r'^stack/(?P<pk>[0-9]+)/edit/$', views.stack_edit, name='stack_edit'),

    url(r'^stackdel/(?P<pk>\d+)$', views.stack_delete, name='stack_delete'),     


    url(r'^switch/new/$', views.switch_new, name='switch_new'),

    url(r'^switch/(?P<pk>[0-9]+)/edit/$', views.switch_edit, name='switch_edit'),

    url(r'^switchdel/(?P<pk>\d+)$', views.switch_delete, name='switch_delete'),      


    url(r'^switchport/new/$', views.switchport_new, name='switchport_new'),

    url(r'^switchport/(?P<pk>[0-9]+)/edit/$', views.switchport_edit, name='switchport_edit'),

    url(r'^switchportdel/(?P<pk>\d+)$', views.switchport_delete, name='switchport_delete'),       


    url(r'^netpoint/new/$', views.netpoint_new, name='netpoint_new'),

    url(r'^netpoint/(?P<pk>[0-9]+)/edit/$', views.netpoint_edit, name='netpoint_edit'),

    url(r'^netpointdel/(?P<pk>\d+)$', views.netpoint_delete, name='netpoint_delete'),        


    url(r'^user/new/$', views.user_new, name='user_new'),

    url(r'^user/(?P<pk>[0-9]+)/edit/$', views.user_edit, name='user_edit'),    

    url(r'^password/$', views.change_password, name='password'),


    url(r'^ownerid/new/$', views.ownerid_new, name='ownerid_new'),

    url(r'^ownerid/(?P<pk>[0-9]+)/edit/$', views.ownerid_edit, name='ownerid_edit'),        


    url(r'^vlan/new/$', views.vlan_new, name='vlan_new'),

    url(r'^vlan/(?P<pk>[0-9]+)/edit/$', views.vlan_edit, name='vlan_edit'),

    url(r'^vlandel/(?P<pk>\d+)$', views.vlan_delete, name='vlan_delete'),           



    url(r'^ownerid-autocomplete/$', OwneridAutocomplete.as_view(create_field='num'), name='ownerid-autocomplete',
    ),

    url(r'^os-autocomplete/$', OsAutocomplete.as_view(), name='os-autocomplete',
    ),

    url(r'^hosttype-autocomplete/$', HosttypeAutocomplete.as_view(create_field='name'), name='hosttype-autocomplete',
    ),        

    url(r'^manufactorer-autocomplete/$', ManufactorerAutocomplete.as_view(create_field='name'), name='manufactorer-autocomplete',
    ), 

    url(r'^place-autocomplete/$', PlaceAutocomplete.as_view(), name='place-autocomplete',
    ),    

    url(r'^stack-autocomplete/$', StackAutocomplete.as_view(), name='stack-autocomplete',
    ), 

    url(r'^network-autocomplete/$', NetworkAutocomplete.as_view(), name='network-autocomplete',
    ), 

    url(r'^ip-autocomplete/$', IpAutocomplete.as_view(), name='ip-autocomplete',
    ),    

    url(r'^host-autocomplete/$', HostAutocomplete.as_view(), name='host-autocomplete',
    ),  

    url(r'^host-autocomplete2/$', HostAutocomplete2.as_view(), name='host-autocomplete2',
    ),

    url(r'^device-autocomplete/$', DeviceAutocomplete.as_view(), name='device-autocomplete',
        ),

    #url(r'^hostphone-autocomplete/$', HostPhoneAutocomplete.as_view(), name='hostphone-autocomplete',
    #),      


    url(r'^device-autocomplete/$', DeviceAutocomplete.as_view(), name='device-autocomplete',
    ),

    url(r'^servicecategory-autocomplete/$', ServicecategoryAutocomplete.as_view(create_field='name'), name='servicecategory-autocomplete',
    ),   

    #url(r'^user-autocomplete/$', UserAutocomplete.as_view(), name='user-autocomplete',    ),

    url(r'^switch-autocomplete/$', SwitchAutocomplete.as_view(create_field='name'), name='switch-autocomplete',
    ),  

    url(r'^switchport-autocomplete/$', SwitchportAutocomplete.as_view(), name='switchport-autocomplete',
    ),       

    url(r'^switchrack-autocomplete/$', SwitchrackAutocomplete.as_view(create_field='name'), name='switchrack-autocomplete',
    ),     

    url(r'^patchpanel-autocomplete/$', PatchpanelAutocomplete.as_view(create_field='num'), name='patchpanel-autocomplete',
    ),        

    url(r'^patchpanelport-autocomplete/$', PatchpanelportAutocomplete.as_view(create_field='num'), name='patchpanelport-autocomplete',
    ),     

    url(r'^phone-autocomplete/$', PhoneAutocomplete.as_view(), name='phone-autocomplete',
    ),        

    url(r'^rack-autocomplete/$', RackAutocomplete.as_view(create_field='name'), name='rack-autocomplete',
    ),           

    url(r'^user-autocomplete/$', UserAutocomplete.as_view(), name='user-autocomplete',
    ),           

    url(r'^devicemodel-autocomplete/$', DevicemodelAutocomplete.as_view(), name='devicemodel-autocomplete',
    ),           

    url(r'^floor-autocomplete/$', FloorAutocomplete.as_view(), name='floor-autocomplete',
    ),  

    url(r'^sector-autocomplete/$', SectorAutocomplete.as_view(), name='sector-autocomplete',
    ),  

    url(r'^phonecategory-autocomplete/$', PhonecategoryAutocomplete.as_view(), name='phonecategory-autocomplete',
    ),  

    url(r'^phonetype-autocomplete/$', PhonetypeAutocomplete.as_view(), name='phonetype-autocomplete',
    ), 

    url(r'^vlan-autocomplete/$', VlanAutocomplete.as_view(), name='vlan-autocomplete',
    ),    

    url(r'^placemodal/', PlaceCreateModal.as_view(), name='placemodal'),      

    url(r'^sectormodal/', SectorCreateModal.as_view(), name='sectormodal'),
    
    url(r'^ipmodal/', IpCreateModal.as_view(), name='ipmodal'),      

    url(r'^servicemodal/', ServiceCreateModal.as_view(), name='servicemodal'),          

    url(r'^servicecatmodal/', ServiceCategoryCreateModal.as_view(), name='servicecategorymodal'),    

    url(r'^floormodal/', FloorCreateModal.as_view(), name='floormodal'),  

    url(r'^usermodal/', UserCreateModal.as_view(), name='usermodal'), 

    url(r'^owneridmodal/', OwneridCreateModal.as_view(), name='owneridmodal'), 

    url(r'^manufactorermodal/', ManufactorerCreateModal.as_view(), name='manufactorermodal'), 

    url(r'^rackmodal/', RackCreateModal.as_view(), name='rackmodal'),     

    url(r'^stackmodal/', StackCreateModal.as_view(), name='stackmodal'),   

    url(r'^switchmodal/', SwitchCreateModal.as_view(), name='switchmodal'),       

    url(r'^hostmodal/', HostCreateModal.as_view(), name='hostmodal'),           

    url(r'^networkmodal/', NetworkCreateModal.as_view(), name='networkmodal'),    

    url(r'^patchpanelmodal/', PatchpanelCreateModal.as_view(), name='patchpanelmodal'),

    url(r'^patchpanelportmodal/', PatchpanelportCreateModal.as_view(), name='patchpanelportmodal'),

    url(r'^osmodal/', OsCreateModal.as_view(), name='osmodal'),

    url(r'^hosttypemodal/', HosttypeCreateModal.as_view(), name='hosttypemodal'),

    url(r'^phonecatmodal/', PhonecategoryCreateModal.as_view(), name='phonecatmodal'),    

    url(r'^phonetypemodal/', PhonetypeCreateModal.as_view(), name='phonetypemodal'),        

    url(r'^switchportmodal/', SwitchportCreateModal.as_view(), name='switchportmodal'),    

    url(r'^devicemodelmodal/', DevicemodelCreateModal.as_view(), name='devicemodelmodal'),    

    url(r'^phonemodal/', PhoneCreateModal.as_view(), name='phonemodal'),  

    url(r'^vlanmodal/', VlanCreateModal.as_view(), name='vlanmodal'),  


    url(r'^sendpassword/(?P<pk>[0-9]+)', views.send_password, name='sendpassword'),

    #telas de erro

  

]
