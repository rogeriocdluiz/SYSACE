# -*- coding: utf-8 -*-

#from django.db import models
#from django.forms import ModelForm
from django import forms  
from django.forms import ModelForm, TextInput, Select, CheckboxInput, NumberInput, SelectMultiple, NullBooleanSelect, CheckboxInput, URLInput, NumberInput, DateInput, EmailInput, Textarea, PasswordInput
from ace.models import *

from django.contrib.auth.models import User, Group

from django.forms import ModelChoiceField, ModelMultipleChoiceField

#from django.utils.translation import ugettext_lazy as _
#from django.core.urlresolvers import reverse_lazy

from dal import autocomplete

from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm


class UserModelChoiceField(ModelChoiceField):
    ''' 
    A ModelChoiceField to represent User 
    select boxes in the Auto Admin 
    '''
    def label_from_instance(self, obj):
        return "%s (%s)"%(obj.get_full_name(), obj.username)



class ConfigForm(forms.ModelForm):

    class Meta:
        model = AceConfig
        fields = '__all__'
        widgets = {
        'org':TextInput(attrs={'class': u'form-control'}),
        'email_from':EmailInput(attrs={'class': u'form-control'}),  
        'email_co':EmailInput(attrs={'class': u'form-control'}),  
        'password_email_text':Textarea(attrs={'class': u'form-control'}),
        'password_email_html_text':Textarea(attrs={'class': u'form-control' }),
        'phonelist_results':NumberInput(attrs={'class': u'form-control'}),
        'hostlist_results':NumberInput(attrs={'class': u'form-control'}),
        'iplist_results':NumberInput(attrs={'class': u'form-control'}),
        'networklist_results':NumberInput(attrs={'class': u'form-control'}),
        'netpointlist_results':NumberInput(attrs={'class': u'form-control'}),
        'owneridlist_results':NumberInput(attrs={'class': u'form-control'}),
        'patchpanel_results':NumberInput(attrs={'class': u'form-control'}),
        'placelist_results':NumberInput(attrs={'class': u'form-control'}),
        'racklist_results':NumberInput(attrs={'class': u'form-control'}),
        'sectorlist_results':NumberInput(attrs={'class': u'form-control'}),
        'servicelist_results':NumberInput(attrs={'class': u'form-control'}),
        'stacklist_results':NumberInput(attrs={'class': u'form-control'}),
        'switchlist_results':NumberInput(attrs={'class': u'form-control'}),
        'userlist_results':NumberInput(attrs={'class': u'form-control'}),
        'printerlist_results':NumberInput(attrs={'class': u'form-control'}),
        }  



class HostForm(forms.ModelForm):
	#name = forms.CharField(widget=forms.TextInput(attrs={'class': u'form-control'}))
	#ownerid = forms.Select(widget=forms.TextInput(attrs={'class': u'form-control'}))
    ownerid = forms.ModelChoiceField(
        queryset=Ownerid.objects.all(),
        widget=autocomplete.ModelSelect2(url='ownerid-autocomplete',attrs={'class': u'form-control'},),
        label=u'Patrimônio',
        required=False
    )
    os = forms.ModelChoiceField(
        queryset=Os.objects.all(),
        widget=autocomplete.ModelSelect2(url='os-autocomplete',attrs={'class': u'form-control'},),
        label=u'Sistema Operacional',
        required=False
    )
    
    manufactorer = forms.ModelChoiceField(
        queryset=Manufactorer.objects.all(),
        widget=autocomplete.ModelSelect2(url='manufactorer-autocomplete',attrs={'class': u'form-control'},),
        label=u'Fabricante',
        required=False
    )   

    place = forms.ModelChoiceField(
        queryset=Place.objects.all(),
        widget=autocomplete.ModelSelect2(url='place-autocomplete',attrs={'class': u'form-control'},),
        label=u'Local',
        required=False,
        help_text=u"Onde o equipamento está instalado (Não se aplica à máquinas virtuais)"
    )

    devicemodel = forms.ModelChoiceField(
        queryset=Devicemodel.objects.all(),
        widget=autocomplete.ModelSelect2(url='devicemodel-autocomplete',attrs={'class': u'form-control'},),
        label=u'Modelo do equipamento',
        required=False
    )   


    admuser = forms.CharField(
        widget=forms.TextInput(attrs={'class': u'form-control'},),
        required=False,
        label=u'Usuário administrador'
    )         
    admpass = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': u'form-control'},),
        required=False,
        label=u'Senha do administrador'
    )
    

    class Meta:
		model = Host
		#fields = '__all__'
		fields = ['name','active','vm','supplierhw', 'ownerid','serial_number','devicemodel','osplatform','os','hwtype','manufactorer','place','url', 'admuser','admpass','mem','cpu','groups','comments'] 
		widgets = {
        'name': TextInput(attrs={'class': u'form-control'}),
        'active': CheckboxInput(attrs={'class': u'form-control'}),
        'vm': CheckboxInput(attrs={'class': u'form-control'}),
        'supplierhw': CheckboxInput(attrs={'class': u'form-control'}),
        'osplatform':Select(attrs={'class': u'form-control'}),
        'hwtype':Select(attrs={'class': u'form-control'}),
        'url':URLInput(attrs={'class': u'form-control'}),  
        'serial_number':TextInput(attrs={'class': u'form-control'}),
        'devicemodel':Select(attrs={'class': u'form-control'}),
        'place':Select(attrs={'class': u'form-control'}),
        'mem':TextInput(attrs={'class': u'form-control'}),
        'cpu':NumberInput(attrs={'class': u'form-control'}),
        'manufactorer':Select(attrs={'class': u'form-control'}),
        'groups':SelectMultiple(attrs={'class': u'form-control'}),
        'comments':Textarea(attrs={'class': u'form-control'}), 
    	}





class PrinterForm(forms.ModelForm):

    ownerid = forms.ModelChoiceField(
        queryset=Ownerid.objects.all(),
        widget=autocomplete.ModelSelect2(url='ownerid-autocomplete',attrs={'class': u'form-control'},),
        label=u'Patrimônio',
        required=False
    )
    manufactorer = forms.ModelChoiceField(
        queryset=Manufactorer.objects.all(),
        widget=autocomplete.ModelSelect2(url='manufactorer-autocomplete',attrs={'class': u'form-control'},),
        label=u'Fabricante',
        required=False
    )       

    place = forms.ModelChoiceField(
        queryset=Place.objects.all(),
        widget=autocomplete.ModelSelect2(url='place-autocomplete',attrs={'class': u'form-control'},),
        label=u'Local',
        required=False,
        help_text=u"Onde o equipamento está instalado"
    )

       
    admuser = forms.CharField(
        widget=forms.TextInput(attrs={'class': u'form-control'},),
        required=False,
        label=u'Usuário administrador'
    )         
    admpass = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': u'form-control'},),
        required=False,
        label=u'Senha do administrador'
    )    


    devicemodel = forms.ModelChoiceField(
        queryset=Devicemodel.objects.all(),
        widget=autocomplete.ModelSelect2(url='devicemodel-autocomplete',attrs={'class': u'form-control'},),
        label=u'Modelo do equipamento',
        required=False
    )      

    class Meta:
        model = Printer
        fields = ['name','supplierhw','ownerid','active','serial_number', 'manufactorer','printer_type','devicemodel','place','url','admuser','admpass','groups','comments',]
        exclude = ['osplatform','vm']
        widgets = {
        'name': TextInput(attrs={'class': u'form-control'}),
        'supplierhw': CheckboxInput(attrs={'class': u'form-control'}),
        'active': CheckboxInput(attrs={'class': u'form-control'}),
        'url':URLInput(attrs={'class': u'form-control'}),  
        'serial_number':TextInput(attrs={'class': u'form-control'}),
        #'model':TextInput(attrs={'class': u'form-control'}),
        'devicemodel':Select(attrs={'class': u'form-control'}),
        'printer_type':Select(attrs={'class': u'form-control'}),
        'manufactorer':Select(attrs={'class': u'form-control'}),
        'place':Select(attrs={'class': u'form-control'}),
        'groups':SelectMultiple(attrs={'class': u'form-control'}),        
        'comments':Textarea(attrs={'class': u'form-control'}),         

        } 





class HostFormModal(forms.ModelForm):
       
    admuser = forms.CharField(
        widget=forms.TextInput(attrs={'class': u'form-control'},),
        required=False,
        label=u'Usuário administrador'
    )         
    admpass = forms.CharField(
        widget=forms.TextInput(attrs={'class': u'form-control'},),
        required=False,
        label=u'Senha do administrador'
    )
    

    class Meta:
        model = Host
        fields = ['name','supplierhw','ownerid','serial_number','osplatform','os','hwtype','manufactorer','place','vm', 'url', 'admuser','admpass','mem','cpu','comments'] 
        widgets = {
        'name': TextInput(attrs={'class': u'form-control'}),
        'ownerid':Select(attrs={'class': u'form-control'}),
        'osplatform':Select(attrs={'class': u'form-control'}),
        'hwtype':Select(attrs={'class': u'form-control'}),
        'url':URLInput(attrs={'class': u'form-control'}),  
        'serial_number':TextInput(attrs={'class': u'form-control'}),
        'model':TextInput(attrs={'class': u'form-control'}),
        'place':Select(attrs={'class': u'form-control'}),
        'os':Select(attrs={'class': u'form-control'}),
        'mem':TextInput(attrs={'class': u'form-control'}),
        'cpu':NumberInput(attrs={'class': u'form-control'}),
        'manufactorer':Select(attrs={'class': u'form-control'}),
        'comments':Textarea(attrs={'class': u'form-control'}), 
        
        }








class ServiceForm(forms.ModelForm):
    network = forms.ModelChoiceField(
        queryset=Network.objects.all(),
        widget=autocomplete.ModelSelect2(url='network-autocomplete',attrs={'class': u'form-control'},),
        label=u'Rede'
    ) 
    #category = forms.ModelChoiceField(
    #    queryset=Servicecategory.objects.all(),
    #    widget=autocomplete.ModelSelect2Multiple(url='servicecategory-autocomplete',attrs={'class': u'form-control'},),
    #    label=u'Categoria'
    #)        

    class Meta:
        model = Service
        fields = ['name','network','ip','category','obs']
        widgets = {
        'name':TextInput(attrs={'class': u'form-control'}),
        #'network':Select(attrs={'class': u'form-control'}),
        #'ip':Select(attrs={'class': u'form-control'}),
        'ip': autocomplete.ModelSelect2(url='ip-autocomplete',forward=['network'],attrs={'class': u'form-control'},),        
        'category':SelectMultiple(attrs={'class': u'form-control'}),
        'obs':Textarea(attrs={'class': u'form-control'}),
        }


class ServiceFormModal(forms.ModelForm):
    

    class Meta:
        model = Service
        fields = '__all__'
        widgets = {
        'name':TextInput(attrs={'class': u'form-control'}),
        'network':Select(attrs={'class': u'form-control'}),
        'ip':Select(attrs={'class': u'form-control'}),
        'category':SelectMultiple(attrs={'class': u'form-control'}),
        'obs':TextInput(attrs={'class': u'form-control'}),
        }



class ServiceCategoryFormModal(forms.ModelForm):
    

    class Meta:
        model = Servicecategory
        fields = '__all__'
        widgets = {
        'name':TextInput(attrs={'class': u'form-control'}),
        }





class NetworkForm(forms.ModelForm):
    

    class Meta:
        model = Network
        fields = ['name','address','mask', 'gateway','vln', 'dhcp','dhcp_start','dhcp_end','comments']
        widgets = {
        'name':TextInput(attrs={'class': u'form-control'}),
        'address':TextInput(attrs={'class': u'form-control'}),
        'mask':NumberInput(attrs={'class': u'form-control'}),
        'gateway':TextInput(attrs={'class': u'form-control'}),
        'vln':Select(attrs={'class': u'form-control'}),
        'dhcp':CheckboxInput(attrs={'class': u'form-control'}),
        'dhcp_start':TextInput(attrs={'class': u'form-control'}),
        'dhcp_end':TextInput(attrs={'class': u'form-control'}),
        'comments':Textarea(attrs={'class': u'form-control'}), 
        }


class IpForm(forms.ModelForm):

    address = forms.CharField(
        widget=forms.TextInput(attrs={'class': u'form-control'},),
        required=True,
        label=u'Endereço IP'
    )        


    network = forms.ModelChoiceField(
        queryset=Network.objects.all(),
        widget=autocomplete.ModelSelect2(url='network-autocomplete',attrs={'class': u'form-control'},),
        label=u'Rede',
        required=True
    )   
    device = forms.ModelChoiceField(
        queryset=Device.objects.all(),
        widget=autocomplete.ModelSelect2(url='device-autocomplete',attrs={'class': u'form-control'},),
        label=u'Equipamento/Servidor'
    )         

    class Meta:
        model = Ip
        fields = ['address','network','device','comments']
        widgets = {
        'address':TextInput(attrs={'class': u'form-control'}),
        'network':Select(attrs={'class': u'form-control'}),
        'device':Select(attrs={'class': u'form-control'}),
        'comments':Textarea(attrs={'class': u'form-control'}),
        }        


class IpFormnew(forms.ModelForm):


#    address = forms.CharField(
#       widget = forms.HiddenInput(), required = False
#    )

#    network = forms.CharField(
#        widget = forms.HiddenInput(), required = False
#    )


    device = forms.ModelChoiceField(
        queryset=Device.objects.all(),
        widget=autocomplete.ModelSelect2(url='device-autocomplete',attrs={'class': u'form-control'},),
        label=u'Equipamento/Servidor'
    )         


    class Meta:
        model = Ip
        fields = ['device','comments']
        widgets = {
        'address':TextInput(attrs={'class': u'form-control'}),
        'network':Select(attrs={'class': u'form-control'}),
        'device':Select(attrs={'class': u'form-control'}),
        'comments':Textarea(attrs={'class': u'form-control'}),
        }  

             

class IpFormModal(forms.ModelForm):
    
    class Meta:
        model = Ip
        fields = ['address','network','device']
        widgets = {
        'address':TextInput(attrs={'class': u'form-control'}),
        'network':Select(attrs={'class': u'form-control'}),
        'device':Select(attrs={'class': u'form-control'}),        
        }    







#class PhoneForm(forms.ModelForm):


#    place = forms.ModelChoiceField(
        #queryset=Place.objects.all(),
        #widget=autocomplete.ModelSelect2(url='place-autocomplete',attrs={'class': u'form-control'},),
        #label=u'Local',
        #required=False,
    #help_text='Local onde o telefone está instalado (Não se aplica a senhas)'

    #)

#    phonecategory = forms.ModelChoiceField(
        #queryset=Phonecategory.objects.all(),
        #widget=autocomplete.ModelSelect2(url='phonecategory-autocomplete',attrs={'class': u'form-control'},),
        #label=u'Categoria do telefone',
        #required=False,
        #help_text='Indica o tipo de chamada telefônica permitida'

    #)

    #telephonetype = forms.ModelChoiceField(
    #    queryset=Phonetype.objects.all(),
    #    widget=autocomplete.ModelSelect2(url='phonetype-autocomplete',attrs={'class': u'form-control'},),
    #    label=u'Tipo/tecnologia do telefone',
    #    required=False,
    #    help_text="Digital, analógico, IP"
    #)



    #class Meta:
    #    model = Phone
    #    fields = ['num','place','password', 'phonecategory','telephonetype',  'dg', 'dist', 'bloco', 'par','comments']
    #    widgets = {
    #    'num':TextInput(attrs={'class': u'form-control'}),
    #    'password':CheckboxInput(attrs={'class': u'form-control','id':'password', 'onclick': 'javascript:passwordCheck();'}),
    #    'active':CheckboxInput(attrs={'class': u'form-control'}),     
    #    'newpassword':NullBooleanSelect(attrs={'class': u'form-control'}),  
    #    'phonecategory':Select(attrs={'class': u'form-control'}),        
    #    'telephonetype':Select(attrs={'class': u'form-control'}),  
    #    'dist': TextInput(attrs={'class': u'form-control'}),
    #    'bloco': TextInput(attrs={'class': u'form-control'}),
    #    'par': TextInput(attrs={'class': u'form-control'}),
    #    'dg': TextInput(attrs={'class': u'form-control'}),              
    #    'comments':Textarea(attrs={'class': u'form-control'}), 
    #    }         






class PhoneForm(forms.ModelForm):


    place = forms.ModelChoiceField(
        queryset=Place.objects.all(),
        widget=autocomplete.ModelSelect2(url='place-autocomplete',attrs={'class': u'form-control'},),
        label=u'Local',
        required=False,
        help_text='Local onde o telefone está instalado (Não se aplica a senhas)'

    )        

    phonecategory = forms.ModelChoiceField(
        queryset=Phonecategory.objects.all(),
        widget=autocomplete.ModelSelect2(url='phonecategory-autocomplete',attrs={'class': u'form-control'},),
        label=u'Categoria',
        required=False,
        help_text='Indica o tipo de chamada telefônica permitida'

    )

    telephonetype = forms.ModelChoiceField(
        queryset=Phonetype.objects.all(),
        widget=autocomplete.ModelSelect2(url='phonetype-autocomplete',attrs={'class': u'form-control'},),
        label=u'Tipo/tecnologia do telefone',
        required=False,
        help_text="Digital, analógico, IP - Somente telefones"
    )

    user = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=autocomplete.ModelSelect2(url='user-autocomplete',attrs={'class': u'form-control'},),
        label=u'Usuário',
        required=False,    
    ) 

    # host = forms.ModelChoiceField(
    #    queryset=Host.objects.all(),
    #    widget=autocomplete.ModelSelect2(url='hostphone-autocomplete',attrs={'class': u'form-control'},),
    #    label=u'Equipamento/Aperelho telefônico',
    #    required=False,    
    #)     


    class Meta:
        model = Phone
        fields = ['num','place','password', 'phonecategory','telephonetype','user', 'phonehw','dg', 'dist', 'bloco', 'par','comments']
        widgets = {
        'num':TextInput(attrs={'class': u'form-control'}),
        'password':CheckboxInput(attrs={'class': u'form-control','id':'password', 'onclick': 'javascript:passwordCheck();'}),
        'active':CheckboxInput(attrs={'class': u'form-control'}),     
        #'newpassword':NullBooleanSelect(attrs={'class': u'form-control'}),  
        'phonecategory':Select(attrs={'class': u'form-control'}),        
        'telephonetype':Select(attrs={'class': u'form-control'}),  
        'phonehw': TextInput(attrs={'class': u'form-control'}),
        'dist': TextInput(attrs={'class': u'form-control'}),
        'bloco': TextInput(attrs={'class': u'form-control'}),
        'par': TextInput(attrs={'class': u'form-control'}),
        'dg': TextInput(attrs={'class': u'form-control'}),              
        'comments':Textarea(attrs={'class': u'form-control'}), 
        'user':Select(attrs={'class': u'form-control'}),
        }   



    def __init__(self, *args, **kwargs):
        super(PhoneForm, self).__init__(*args, **kwargs)
        self.fields['user'].queryset = User.objects.order_by('username')  
#        self.fields['user'].label_from_instance = lambda obj: "%s" % obj.get_full_name()









class PhonetypeForm(forms.ModelForm):

    name = forms.CharField(
        label='Nome',
        widget=forms.TextInput(attrs={'class': u'form-control'},),
    )

    class Meta:
        model = Phonetype
        fields = '__all__'  
        widgets = {
        'comments':Textarea(attrs={'class': u'form-control'}), 
        }             







class PlaceForm(forms.ModelForm):

    floor = forms.ModelChoiceField(
        queryset=Floor.objects.all(),
        widget=autocomplete.ModelSelect2(url='floor-autocomplete',attrs={'class': u'form-control'},),
        label=u'Andar',
        required=True
    )


    sector = forms.ModelChoiceField(
        queryset=Sector.objects.all(),
        widget=autocomplete.ModelSelect2(url='sector-autocomplete',attrs={'class': u'form-control'},),
        label=u'Setor/Departamento',
        required=False
    )


    class Meta:
        model = Place
        fields = ['name','placetype','floor','sector','comments']
        widgets = {
        'name':TextInput(attrs={'class': u'form-control'}),
        'placetype':Select(attrs={'class': u'form-control'}),   
        'floor':Select(attrs={'class': u'form-control'}),   
        'sector':Select(attrs={'class': u'form-control'}),
        #'side':Select(attrs={'class': u'form-control'}),              
        'comments':Textarea(attrs={'class': u'form-control'}), 
        } 

class SectorFormModal(forms.ModelForm):

    class Meta:
        model = Sector
        fields = ['name','comments']
        widgets = {
        'name':TextInput(attrs={'class': u'form-control'}),
        'comments':Textarea(attrs={'class': u'form-control'}), 
        }



class FloorFormModal(forms.ModelForm):

    name = forms.CharField(
        label='Nome',
        widget=forms.TextInput(attrs={'class': u'form-control'},),
    )

    class Meta:
        model = Floor
        fields = '__all__'               


class RackForm(forms.ModelForm):
    place = forms.ModelChoiceField(
        queryset=Place.objects.all(),
        widget=autocomplete.ModelSelect2(url='place-autocomplete',attrs={'class': u'form-control'},),
        label=u'Local'
    )    

    class Meta:
        model = Rack
        fields = ['name','place']
        widgets = {
        'name':TextInput(attrs={'class': u'form-control'}),
    #    'place':Select(attrs={'class': u'form-control'}),   
        }          


class RackFormModal(forms.ModelForm):    

    class Meta:
        model = Rack
        fields = '__all__'
        widgets = {
        'name':TextInput(attrs={'class': u'form-control'}),
        'place':Select(attrs={'class': u'form-control'}),   
        }          





class StackForm(forms.ModelForm):

    admuser = forms.CharField(
    widget=forms.TextInput(attrs={'class': u'form-control'},),
    required=False,
    label=u'Usuário administrador'
    )         
    admpass = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': u'form-control'},),
        required=False,
        label=u'Senha do administrador'
    )

    class Meta:
        model = Stack
        fields = ['name','url','admuser','admpass','comments']
        widgets = {
        'name':TextInput(attrs={'class': u'form-control'}),
        'url':URLInput(attrs={'class': u'form-control'}),  
        'admuser':TextInput(attrs={'class': u'form-control'}),  
        'admpass':TextInput(attrs={'class': u'form-control'}),  
        'comments':Textarea(attrs={'class': u'form-control'}), 
        }            


class StackFormModal(forms.ModelForm):
       
    admpass = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': u'form-control'},),
        required=False,
        label=u'Senha do administrador'
    )

    class Meta:
        model = Stack
        fields = ['name','url','admuser','admpass','comments']
        widgets = {
        'name':TextInput(attrs={'class': u'form-control'}),
        'url':URLInput(attrs={'class': u'form-control'}),  
        'admuser':TextInput(attrs={'class': u'form-control'}),  
        'admpass':TextInput(attrs={'class': u'form-control'}),  
        'comments':Textarea(attrs={'class': u'form-control'}),  
        }      



class SwitchForm(forms.ModelForm):

    ownerid = forms.ModelChoiceField(
        queryset=Ownerid.objects.all(),
        widget=autocomplete.ModelSelect2(url='ownerid-autocomplete',attrs={'class': u'form-control'},),
        label=u'Patrimônio',
        required=False,
    )    
    manufactorer = forms.ModelChoiceField(
        queryset=Manufactorer.objects.all(),
        widget=autocomplete.ModelSelect2(url='manufactorer-autocomplete',attrs={'class': u'form-control'},),
        label=u'Fabricante'
    )
    place = forms.ModelChoiceField(
        queryset=Place.objects.all(),
        widget=autocomplete.ModelSelect2(url='place-autocomplete',attrs={'class': u'form-control'},),
        label=u'Local',
        required=False,
    )
    admuser = forms.CharField(
        widget=forms.TextInput(attrs={'class': u'form-control'},),
        required=False,
        label=u'Usuário administrador'
    )         
    admpass = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': u'form-control'},),
        required=False,
        label=u'Senha do administrador'
    )      
    stack_field = forms.ModelChoiceField(
        queryset=Stack.objects.all(),
        widget=autocomplete.ModelSelect2(url='stack-autocomplete',attrs={'class': u'form-control'},),
        label=u'Pilha',
        required=False
    )

    devicemodel = forms.ModelChoiceField(
        queryset=Devicemodel.objects.all(),
        widget=autocomplete.ModelSelect2(url='devicemodel-autocomplete',attrs={'class': u'form-control'},),
        label=u'Modelo do equipamento',
        required=False
    )

    #rack = forms.ModelChoiceField(
    #    queryset=Rack.objects.all(),
    #    widget=autocomplete.ModelSelect2(url='rack-autocomplete',forward=['place'],attrs={'class': u'form-control'},),
    #    label=u'Rack',
    #    required=True
    #)


    class Meta:
        model = Switch
        fields =  ['name','active', 'ownerid', 'devicemodel', 'manufactorer','serial','devicemodel','serial','place','rack','ports','manageable','url','admuser','admpass','stacked','stack_field','comments']
        #fields = '__all__'
        widgets = {
        'name':TextInput(attrs={'class': u'form-control'}),
        'active': CheckboxInput(attrs={'class': u'form-control'}),
        #'ownerid':Select(attrs={'class': u'form-control'}),
        #'manufactorer':Select(attrs={'class': u'form-control'}),
        'serial':TextInput(attrs={'class': u'form-control'}),  
        #'model':TextInput(attrs={'class': u'form-control'}),  
        'devicemodel':Select(attrs={'class': u'form-control'}),
        #'place':Select(attrs={'class': u'form-control'}),   
        #'rack':Select(attrs={'class': u'form-control'}),
        'rack': autocomplete.ModelSelect2(url='rack-autocomplete',forward=['place'],attrs={'class': u'form-control'},),
        'ports': NumberInput(attrs={'class': u'form-control'}),
        'manageable':CheckboxInput(attrs={'class': u'form-control'}),     
        'url':URLInput(attrs={'class': u'form-control'}),
        'admpass':TextInput(attrs={'class': u'form-control'}),
        'stacked':CheckboxInput(attrs={'class': u'form-control'}), 
        #'stack':Select(attrs={'class': u'form-control'}),
        'comments':Textarea(attrs={'class': u'form-control'}), 
        }   





class SwitchFormModal(forms.ModelForm):
        
    admpass = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': u'form-control'},),
        required=False,
        label=u'Senha do administrador'
    )    

    devicemodel = forms.ModelChoiceField(
        queryset=Devicemodel.objects.all(),
        widget=autocomplete.ModelSelect2(url='devicemodel-autocomplete',attrs={'class': u'form-control'},),
        label=u'Modelo do equipamento',
        required=False
    )      
    

    class Meta:
        model = Switch
        fields =  ['name','ownerid', 'manufactorer','serial','devicemodel','place','rack','ports','manageable','url','admuser','admpass','stacked','stack_field','comments']
        widgets = {
        'name':TextInput(attrs={'class': u'form-control'}),
        'ownerid':Select(attrs={'class': u'form-control'}),
        'manufactorer':Select(attrs={'class': u'form-control'}),
        'serial':TextInput(attrs={'class': u'form-control'}),  
        #'model':TextInput(attrs={'class': u'form-control'}),  
        'place':Select(attrs={'class': u'form-control'}),   
        'rack':Select(attrs={'class': u'form-control'}),
        'ports': NumberInput(attrs={'class': u'form-control'}),
        'manageable':CheckboxInput(attrs={'class': u'form-control'}),     
        'url':URLInput(attrs={'class': u'form-control'}),
        'admuser':TextInput(attrs={'class': u'form-control'}),
        'admpass':TextInput(attrs={'class': u'form-control'}),
        'stacked':CheckboxInput(attrs={'class': u'form-control'}), 
        'stack_field':Select(attrs={'class': u'form-control'}),
        'comments':Textarea(attrs={'class': u'form-control'}), 
        }  









class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','is_active','is_staff','groups']
        widgets = {
        'username':TextInput(attrs={'class': u'form-control'}),
        'first_name':TextInput(attrs={'class': u'form-control'}),
        'last_name':TextInput(attrs={'class': u'form-control'}),
        #'password':PasswordInput(attrs={'class': u'form-control'}),
        'email':EmailInput(attrs={'class': u'form-control'}),          
        'is_active':CheckboxInput(attrs={'class': u'form-control'}), 
        'is_staff':CheckboxInput(attrs={'class': u'form-control'}), 
        'groups':SelectMultiple(attrs={'class': u'form-control'}), 
        }

 




class UserFormModal(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username','first_name','last_name','password','email','is_active','is_staff','groups']
        widgets = {
        'username':TextInput(attrs={'class': u'form-control'}),
        'first_name':TextInput(attrs={'class': u'form-control'}),
        'last_name':TextInput(attrs={'class': u'form-control'}),
        'password':PasswordInput(attrs={'class': u'form-control'}),
        'email':EmailInput(attrs={'class': u'form-control'}),          
        'is_active':CheckboxInput(attrs={'class': u'form-control'}), 
        'is_staff':CheckboxInput(attrs={'class': u'form-control'}), 
        'groups':SelectMultiple(attrs={'class': u'form-control'}), 
        
        }  



class NewUserForm(forms.ModelForm):


    class Meta:
        model = User
        fields = ['username','first_name','last_name','password','email','is_active','is_staff','groups']
        widgets = {
        'username':TextInput(attrs={'class': u'form-control'}),
        'first_name':TextInput(attrs={'class': u'form-control'}),
        'last_name':TextInput(attrs={'class': u'form-control'}),
        'password':PasswordInput(attrs={'class': u'form-control'}),
        'email':EmailInput(attrs={'class': u'form-control'}),          
        'is_active':CheckboxInput(attrs={'class': u'form-control'}), 
        'is_staff':CheckboxInput(attrs={'class': u'form-control'}), 
        'groups':SelectMultiple(attrs={'class': u'form-control'}), 
        }  



    def clean_username(self):

        username = self.cleaned_data['username']

        try:
            user_exists = User.objects.get(username=username)
            raise forms.ValidationError(u"Usuario já existe")
        except User.DoesNotExist:
            return username


    def clean_email(self):
        email = self.cleaned_data['email']

        try:
            user_exists = User.objects.get(email=email)
            raise forms.ValidationError(u"Email já existe")
        except User.DoesNotExist:
            return email






class OwneridForm(forms.ModelForm):

    class Meta:
        model = Ownerid
        fields = ['num']
        widgets = {
        'num':TextInput(attrs={'class': u'form-control'}),
        }   




class NetpointForm(forms.ModelForm):

    place = forms.ModelChoiceField(
    queryset=Place.objects.all(),
    widget=autocomplete.ModelSelect2(url='place-autocomplete',attrs={'class': u'form-control'},),
    label=u'Local',
    help_text='localização do ponto de rede'
    )

    rack = forms.ModelChoiceField(
    queryset=Rack.objects.all(),
    widget=autocomplete.ModelSelect2(url='rack-autocomplete',attrs={'class': u'form-control'},),
    label=u'Rack'
    )

    class Meta:
        model = Netpoint
        fields = ['num','pointtype','place', 'rack','switch','swport','patchpanel','patchpanelport','phone','comments']
        widgets = {
        'num':TextInput(attrs={'class': u'form-control'}),
        'pointtype':Select(attrs={'class': u'form-control'}),    
        'rack': Select(attrs={'class': u'form-control'}), 
        'patchpanel': autocomplete.ModelSelect2(url='patchpanel-autocomplete',forward=['rack'],attrs={'class': u'form-control'},),        
        'patchpanelport': autocomplete.ModelSelect2(url='patchpanelport-autocomplete',forward=['patchpanel'],attrs={'class': u'form-control'},),        
        'switch': autocomplete.ModelSelect2(url='switchrack-autocomplete',forward=['rack'],attrs={'class': u'form-control'},),  
        'swport': autocomplete.ModelSelect2(url='switchport-autocomplete',forward=['switch'],attrs={'class': u'form-control'},),  
        'phone': autocomplete.ModelSelect2(url='phone-autocomplete',forward=['place'],attrs={'class': u'form-control'},),  
        'comments':Textarea(attrs={'class': u'form-control'}), 


        }                   
      

class SwitchportForm(forms.ModelForm):

    #vln = forms.ModelChoiceField(
    #queryset=Vlan.objects.all(),
    #widget=autocomplete.ModelSelect2(url='vlan-autocomplete',attrs={'class': u'form-control'},),
    #label=u'VLAN',
    #required=False
    #)    

    switch = forms.ModelChoiceField(
    queryset=Switch.objects.all(),
    widget=autocomplete.ModelSelect2(url='switch-autocomplete',attrs={'class': u'form-control'},),
    label=u'Switch'
    )

    host = forms.ModelChoiceField(
    queryset=Device.objects.all(),
    widget=autocomplete.ModelSelect2(url='device-autocomplete',attrs={'class': u'form-control'},),
    label=u'Equipamento/Host',
    required=False
    )


    class Meta:
        model = Switchport
        fields = ['num','vlans','switch','tipo','host','obs']
        widgets = {
        'num':NumberInput(attrs={'class': u'form-control'}),
        'vlans':SelectMultiple(attrs={'class': u'form-control'}),
        #'vln':Select(attrs={'class': u'form-control'}),  
        'switch': Select(attrs={'class': u'form-control'}), 
        'tipo': Select(attrs={'class': u'form-control'}), 
        'host': Select(attrs={'class': u'form-control'}), 
        'obs':Textarea(attrs={'class': u'form-control'}),          

        }        


class ManufactorerForm(forms.ModelForm):

    class Meta:
        model = Manufactorer
        fields = '__all__'
        widgets = {
        'name':TextInput(attrs={'class': u'form-control'}),
        }          


class PatchpanelForm(forms.ModelForm):

    class Meta:
        model = Patchpanel
        fields = '__all__'
        widgets = {
        'num':TextInput(attrs={'class': u'form-control'}),
        'rack': Select(attrs={'class': u'form-control'}), 
        'ports':NumberInput(attrs={'class': u'form-control'}),
        }          


class PatchpanelportForm(forms.ModelForm):

    class Meta:
        model = Patchpanelport
        fields = '__all__'
        widgets = {
        'num':TextInput(attrs={'class': u'form-control'}),
        'patchpanel': Select(attrs={'class': u'form-control'}), 
        'comments':Textarea(attrs={'class': u'form-control'}),
        }       




#class HosttypeFormModal(forms.ModelForm):

#    class Meta:
#        model = Hosttype
#        fields = '__all__'
#        widgets = {
#        'name':TextInput(attrs={'class': u'form-control'}),
#        }   
              


class OsFormModal(forms.ModelForm):

    class Meta:
        model = Os
        fields = '__all__'
        widgets = {
        'name':TextInput(attrs={'class': u'form-control'}),
        'version':TextInput(attrs={'class': u'form-control'}),
        } 


class PhonecategoryFormModal(forms.ModelForm):

    class Meta:
        model = Phonecategory
        fields = '__all__'
        widgets = {
        'num':TextInput(attrs={'class': u'form-control'}),
        'name':TextInput(attrs={'class': u'form-control'}),
        }      


class SwitchportFormModal(forms.ModelForm):

    host = forms.ModelChoiceField(
    queryset=Host.objects.all(),
    widget=Select(attrs={'class': u'form-control'},),
    label=u'Equipamento/Host',
    required=False
    )


    class Meta:
        model = Switchport
        fields = '__all__'
        widgets = {
        'num':NumberInput(attrs={'class': u'form-control'}),
        'vln':Select(attrs={'class': u'form-control'}),  
        'switch': Select(attrs={'class': u'form-control'}), 
        'tipo': Select(attrs={'class': u'form-control'}), 
        'host': Select(attrs={'class': u'form-control'}), 
        'obs':TextInput(attrs={'class': u'form-control'}),          

        }
     
 

class DevicemodelForm(forms.ModelForm):

    class Meta:
        model = Devicemodel
        fields = '__all__'
        widgets = {
        'name':TextInput(attrs={'class': u'form-control'}),
        'comments':Textarea(attrs={'class': u'form-control'}),           
        }  



#class UserModelChoiceField(forms.ModelChoiceField):
#    def label_from_instance(self, obj):
#         return obj.get_full_name().title()




class PhoneownershipForm(forms.ModelForm):

    user = forms.ModelChoiceField(
    #user = UserModelChoiceField(
        queryset=User.objects.all(),
        widget=autocomplete.ModelSelect2(url='user-autocomplete',attrs={'class': u'form-control'},),
        label=u'Usuário',
        required=True,
    ) 

    phonecategory = forms.ModelChoiceField(
        queryset=Phonecategory.objects.all(),
        widget=autocomplete.ModelSelect2(url='phonecategory-autocomplete',attrs={'class': u'form-control'},),
        label=u'Categoria',
        required=True,
        help_text="Quais ligações pode realizar. Não se aplica a senhas"
    )

    telephonetype = forms.ModelChoiceField(
        queryset=Phonetype.objects.all(),
        widget=autocomplete.ModelSelect2(url='phonetype-autocomplete',attrs={'class': u'form-control'},),
        label=u'Tipo/Tecnologia',
        required=False,
        help_text="Tecnologia da linha. Não se aplica a senhas"
    )

    place = forms.ModelChoiceField(
        queryset=Place.objects.all(),
        widget=autocomplete.ModelSelect2(url='place-autocomplete',attrs={'class': u'form-control'},),
        label=u'Local',
        required=False,
        help_text="Não se aplica a senhas"
    )


    class Meta:
        model = Phoneownership
        #fields = '__all__'
        fields = ['user']
        widgets = {
        #'phone':Select(attrs={'class': u'form-control'}),
        'user':Select(attrs={'class': u'form-control'}),
        }  


    def __init__(self, *args, **kwargs):
        super(PhoneownershipForm, self).__init__(*args, **kwargs)   
        self.fields['user'].queryset = User.objects.order_by('username')  
#        self.fields['user'].label_from_instance = lambda obj: "%s" % obj.get_full_name()


class VlanForm(forms.ModelForm):

    class Meta:
        model = Vlan
        fields = '__all__'
        widgets = {
        'vlanid':TextInput(attrs={'class': u'form-control'}),
        'name':TextInput(attrs={'class': u'form-control'}),
        'comments':Textarea(attrs={'class': u'form-control'}),           
        }         

class UpdateForm(forms.ModelForm):

    class Meta:
        model = Hostupdate
        fields = ['name','aplication_date','comments']
        widgets = {
        'name':TextInput(attrs={'class': u'form-control'}),
        'aplication_date': DateInput(attrs={'class': u'form-control border-input', 'data-provide':'datepicker'}), 
        'comments':Textarea(attrs={'class': u'form-control'}),           
        }                 