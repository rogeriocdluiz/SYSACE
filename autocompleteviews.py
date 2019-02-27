# -*- coding: utf-8 -*-

#from ace.models import Switch, Netpoint, Phone, Switchport, Place, Stack, Rack, Host, Service, Ip, Network, Ownerid, Device, Servicecategory, Os, Hosttype, Manufactorer, Patchpanel, Patchpanelport, Devicemodel

from ace.models import *

from django.contrib.auth.models import User, Group

from dal import autocomplete


class OwneridAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated():
            return Ownerid.objects.none()

        qs = Ownerid.objects.all()

        if self.q:
            qs = qs.filter(num__istartswith=self.q)

        return qs



class PhonecategoryAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated():
            return Phonecategory.objects.none()

        qs = Phonecategory.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs


class PhonetypeAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated():
            return Phonetype.objects.none()

        qs = Phonetype.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs





class OsAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated():
            return Os.objects.none()

        qs = Os.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs


class HosttypeAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated():
            return Hosttype.objects.none()

        qs = Hosttype.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs         



class ServicecategoryAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated():
            return Servicecategory.objects.none()

        qs = Servicecategory.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs  



class ManufactorerAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated():
            return Manufactorer.objects.none()

        qs = Manufactorer.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs      

class DevicemodelAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated():
            return Devicemodel.objects.none()

        qs = Devicemodel.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs   



class PlaceAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated():
            return Place.objects.none()

        qs = Place.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs     



class StackAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated():
            return Stack.objects.none()

        qs = Stack.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs                           

class SwitchAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated():
            return Switch.objects.none()

        qs = Switch.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs     



class NetworkAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated():
            return Network.objects.none()

        qs = Network.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs                           


class FloorAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated():
            return Floor.objects.none()

        qs = Floor.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs  



class SectorAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated():
            return Sector.objects.none()

        qs = Sector.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs  




class IpAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated():
            return Ip.objects.none()

        qs = Ip.objects.all()

        network = self.forwarded.get('network', None)
        if network:
            qs = qs.filter(network=network)


        if self.q:
            qs = qs.filter(address__istartswith=self.q)

        return qs     


#autocomplete para hosts
class HostAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated():
            return Host.objects.none()

        qs = Host.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs          

#autocomplete para vms
class HostAutocomplete2(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated():
            return Host.objects.none()

        qs = Host.objects.filter(vm=False)

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs

# autocomplete para devices
class DeviceAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated():
            return Device.objects.none()

        qs = Device.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs



        #class HostPhoneAutocomplete(autocomplete.Select2QuerySetView):
#    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
#        if not self.request.user.is_authenticated():
#            return Host.objects.none()

#        qs = Host.objects.filter(hwtype='voip')

#        if self.q:
#            qs = qs.filter(name__istartswith=self.q)

#        return qs 



class DeviceAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated():
            return Device.objects.none()

        qs = Device.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs    



class VlanAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated():
            return Vlan.objects.none()

        qs = Vlan.objects.all()

        if self.q:
            qs = qs.filter(vlanid__istartswith=self.q)

        return qs





from django.db.models import Q

class UserAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated():
            return User.objects.none()

        qs = Person.objects.all().order_by('username')

        if self.q:
            #qs = qs.filter(first_name__istartswith=self.q)
            qs = qs.filter(username__istartswith=self.q)

        return qs          



class SwitchportAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated():
            return Switchport.objects.none()

        qs = Switchport.objects.all()

        switch = self.forwarded.get('switch', None)
        if switch:
            qs = qs.filter(switch=switch)


        if self.q:
            qs = qs.filter(num__istartswith=self.q)

        return qs          


class SwitchrackAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated():
            return Switch.objects.none()

        qs = Switch.objects.all()

        rack = self.forwarded.get('rack', None)
        if rack:
            qs = qs.filter(rack=rack)


        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs         


    



class PatchpanelAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated():
            return Patchpanel.objects.none()

        qs = Patchpanel.objects.all()

        rack = self.forwarded.get('rack', None)
        if rack:
            qs = qs.filter(rack=rack)


        if self.q:
            qs = qs.filter(num__istartswith=self.q)

        return qs           


class PatchpanelportAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated():
            return Patchpanelport.objects.none()

        qs = Patchpanelport.objects.all()

        patchpanel = self.forwarded.get('patchpanel', None)
        if patchpanel:
            qs = qs.filter(patchpanel=patchpanel)


        if self.q:
            qs = qs.filter(num__istartswith=self.q)

        return qs          

class PhoneAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated():
            return Phone.objects.none()

        qs = Phone.objects.all()

        place = self.forwarded.get('place', None)
        if place:
            qs = qs.filter(place=place)


        if self.q:
            qs = qs.filter(num__istartswith=self.q)

        return qs      


class RackAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated():
            return Rack.objects.none()

        qs = Rack.objects.all()

        place = self.forwarded.get('place', None)
        if place:
            qs = qs.filter(place=place)


        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs                          