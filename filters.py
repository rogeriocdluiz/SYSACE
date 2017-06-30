# -*- coding: utf-8 -*-

from ace.models import Switch, Netpoint, Phone, Switchport, Place, Stack, Rack, Host, Service, Ip, Network, Ownerid, Device, Servicecategory, User, Patchpanel, Patchpanelport, Phonecategory, Sector, Printer

from django import forms  
from django.forms import ModelForm, TextInput, Select, CheckboxInput, NumberInput, SelectMultiple, NullBooleanSelect, CheckboxInput, URLInput, NumberInput, DateInput, EmailInput, Textarea

from django.contrib.auth.models import User, Group

import django_filters

class HostFilter(django_filters.FilterSet):

    name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Host
        fields = ['active','manufactorer', 'ownerid','vm','serial_number','devicemodel','os','osplatform','hwtype','supplierhw']
        order_by = (
        	('name', 'Nome'),
        	('vm', u'Máquina virtual'),
)
        


class PrinterFilter(django_filters.FilterSet):

    name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Printer
        fields = ['active','manufactorer', 'ownerid','serial_number','model','supplierhw']
        order_by = (
            ('name', 'Nome'),
            ('manufactoerer', 'Fabricante'),
)





class SwitchFilter(django_filters.FilterSet):

    name = django_filters.CharFilter(lookup_expr='icontains')
    model = django_filters.CharFilter(lookup_expr='icontains')
    #active = BooleanFilter(widget=BooleanWidget())


    class Meta:
        model = Switch
        fields = ['active','manufactorer', 'ownerid','devicemodel','stack','manageable','place','rack']
        order_by = (
            ('name', 'Nome'),
    )


class ServiceFilter(django_filters.FilterSet):

    name = django_filters.CharFilter(lookup_expr='icontains')


    class Meta:
        model = Service
        fields = ['network','ip', 'category']
        order_by = (
            ('name', 'Nome'),
            
)   


class PlaceFilter(django_filters.FilterSet):

    name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Place
        fields = ['placetype', 'floor', 'sector']
        order_by = (
            ('name', 'Nome'),
            
)     


class SectorFilter(django_filters.FilterSet):

    name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Sector
        fields = ['name']
        order_by = (
            ('name', 'Nome'),
)  

class NetpointFilter(django_filters.FilterSet):

    num = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Netpoint
        fields = ['pointtype', 'rack', 'patchpanel', 'switch', 'swport', 'place']
        order_by = (
            ('num', 'Número'),
            ('place', 'Local'),
            
)         
 

class OwneridFilter(django_filters.FilterSet):

    num = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Ownerid
        
            

class IpFilter(django_filters.FilterSet):

    address = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Ip
        fields = ['network', 'device']
        order_by = (
            ('address', 'Endereço'),
            ('network', 'Rede'),
            ('device', 'Dispositivo'),
            
)                
 

class RackFilter(django_filters.FilterSet):

    name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Rack
        fields = ['place']
        order_by = (
            ('name', 'Nome'),
            ('place', 'Local'),
)



class PatchpanelFilter(django_filters.FilterSet):

    num = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Patchpanel
        fields = ['rack','rack__place','ports']
        order_by = (
            ('num', 'Patchpanel'),
            ('rack', 'Rack'),
            ('rack__place', 'Local'),
            ('ports', 'Portas PP'),
)


class NetworkFilter(django_filters.FilterSet):

    name = django_filters.CharFilter(lookup_expr='icontains')
    address = django_filters.CharFilter(lookup_expr='icontains')
    vlan = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Network
        fields = ['address','dhcp','vlan']
        order_by = (
            ('name', 'Rede'),
            ('address', 'Endereço'),
            ('dhcp', 'DHCP habilitado'),
            ('vlan', 'VLAN'),
)      

class StackFilter(django_filters.FilterSet):

    name = django_filters.CharFilter(lookup_expr='icontains')
    url = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Network
        fields = ['name','url']
        order_by = (
            ('name', 'Rede'),
            ('url', 'Endereço'),
)          



class PhoneFilter(django_filters.FilterSet):

    num = django_filters.CharFilter(lookup_expr='icontains')
    user__username = django_filters.CharFilter(lookup_expr='icontains')
    user__first_name = django_filters.CharFilter(lookup_expr='icontains')
    user__last_name = django_filters.CharFilter(lookup_expr='icontains')
    
    class Meta:
        model = Phone
        fields = ['place','active','password','newpassword','phonecategory','telephonetype','place']
        order_by = (
            ('num', 'Num'),
            ('user', 'Usuário'),
            ('active', 'Ativo'),
            ('telephonetype', 'Tipo'),
            ('phonecategory', 'Categoria'),
            ('place', 'Local'),

        )
         

class UserFilter(django_filters.FilterSet):

    username = django_filters.CharFilter(lookup_expr='icontains')
    first_name = django_filters.CharFilter(lookup_expr='icontains')
    last_name = django_filters.CharFilter(lookup_expr='icontains')    
    email = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = User
        fields = ['username','first_name','last_name','email']
        order_by = (
            ('first_name', 'Nome'),
            ('last_name', 'Sobrenome'),
            ('email', 'Email')
)           