# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader

from ace.models import *

from django.contrib.auth.models import User, Group

from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse

from django.contrib.auth import logout

from django.contrib.auth.decorators import login_required, permission_required

from django.shortcuts import render_to_response
from django.http import Http404

# Para execucao de scripts externos
import subprocess

# Para relatorio
from .reports import *

from .filters import *

# tratamento de endereços ip
import ipaddress
from ipaddress import ip_address
import re

# para forumlarios

from .forms import *
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404

# autocomplete

from .autocompleteviews import *

# phone aggregation
from django.db.models import Count

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.conf import settings
from ace.models import AceConfig

from itertools import chain

# password change
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm
from django.shortcuts import render, redirect

# para tratamento de data
import re
import datetime
from datetime import timedelta

# django-tables2
from django_tables2 import RequestConfig
from .tables import *
from django_tables2.export.export import TableExport

from django.http import QueryDict

from django_modalview.generic.edit import ModalCreateView
from django_modalview.generic.component import ModalResponse

from mail_templated import EmailMessage

from django.views.generic.list import ListView

from django.http import JsonResponse
from django.template.loader import render_to_string


def addlog(h, e, d, a, t, i):
    #h=host or other action, e=event, d=event_date, a=actor, t=record_type, i=object_id
    log = Log.objects.create(
        record_name=h,
        event=e,
        event_date=d,
        actor=a,
        record_type=t,
        object_id=i
    )
    return log



def sendphone_notification(p, u, d, o):

    erro = ""
    try:
        config = AceConfig.objects.get()
        from_email = config.email_from
        co_email = config.email_co
        to_email = config.email_to

    except:
        erro="erro"

    if p.password==True:
        pwd = "ok"

        if o.active == True:
            m = "associado"
            c = "à"
            d = o.date_activation
        else:
            m = "desassociado"
            c = "da"
            d = o.date_deactivation

    else:
        pwd = "nok"

        if o.active == True:
            m = "associado"
            c = "ao"
            d = o.date_activation
        else:
            m = "desassociado"
            c = "do"
            d = o.date_deactivation

    if erro!="erro":
        message = EmailMessage('email/notification_email.tpl', {'p': p, 'u': u, 'd': d,'m':m, 'c':c, 'pwd':pwd }, from_email, to=[to_email], bcc=[co_email])
        message.send()
    else:
        pass


    return message

@login_required(login_url='/ace/login/')
def index(request):
    usr = request.user
    title = "Painel"

    pd = Netpoint.objects.filter(pointtype='dados')
    pontodados = pd.order_by('num')
    pontodados_modificados = pd.order_by('-modification_date')[:3]
    total_pontodados = pd.count()

    pv = Netpoint.objects.filter(pointtype='voz')
    pontovoz = pv.order_by('num')
    total_pontovoz = pv.count()

    pvoip = Netpoint.objects.filter(pointtype='voip')
    pontovoip = pvoip.order_by('num')
    total_pontovoip = pvoip.count()

    ramal_ativos = Phone.objects.filter(active=True, password=False).order_by('num')
    total_ramal_ativos = ramal_ativos.count()

    pontovoz_modificados = Netpoint.objects.filter(pointtype='voz').order_by('-modification_date')[:3]
    ramal_modificados = Phone.objects.filter(password=False).order_by('-date_modification')[:3]
    senha_modificados = Phone.objects.filter(password=True).order_by('-date_modification')[:3]
    ip_modificados = Ip.objects.filter().order_by('-modification_date')[:3]
    service_modificados = Service.objects.filter().order_by('-modification_date')[:3]
    host_modificados = Host.objects.filter().order_by('-modification_date')[:3]
    switches = Switch.objects.all()
    switch_modificados = switches.order_by('-modification_date')[:3]

    total_ramal_livres = Phone.objects.filter(active=False, password=False).count()
    total_senha_ativos = Phone.objects.filter(password=True, active=True).count()

    senha_livres = Phone.objects.filter(password=True, active=False).count()
    total_switches = switches.count()
    total_pontos = Netpoint.objects.all().count()
    total_printer = Printer.objects.all().count()

    total_phone = Phone.objects.filter(active=True).count()
    total_ramal = Phone.objects.filter(password=False).count()
    total_senha = Phone.objects.filter(password=True).count()
    total_senha_d = Phone.objects.filter(password=True, active=False).count()

    ponto_livres = (total_pontos - (total_pontodados + total_pontovoz + total_pontovoip))
    ponto_ativos = (total_pontos - ponto_livres)
    ramal_livres = (total_ramal - total_ramal_ativos)

    total_service = Service.objects.all().count()
    total_host = Host.objects.all().count()
    total_ip = Ip.objects.all().count()
    host_linux = Host.objects.filter(osplatform='linux').count()
    host_win = Host.objects.filter(osplatform='windows').count()
    host_bsd = Host.objects.filter(osplatform='bsd').count()
    host_other = Host.objects.filter(osplatform='other').count()
    servicecategories = Servicecategory.objects.all()

    phonecats = Phonecategory.objects.annotate(num_phones=Count('phone'))
    phonetypes = Phonetype.objects.annotate(num_phones=Count('phone'))

    logs = Log.objects.all().order_by('-event_date')[:10]

    return render ( request, 'index.html',
        {
        'pontodados_ativos': pontodados,
        'pontovoz_ativos': pontovoz,
        'pontovoip_ativos': pontovoip,
        'ramal_ativos': ramal_ativos,
        'total_pontodados': total_pontodados,
        'total_pontovoz': total_pontovoz,
        'total_pontovoip': total_pontovoip,
        'total_switches': total_switches,
        'total_pontos': total_pontos,
        'total_ramal': total_ramal,
        'total_ramal_livres': total_ramal_livres,
        'total_ramal_ativos': total_ramal_ativos,
        'total_senha': total_senha,
        'total_senha_ativos': total_senha_ativos,
        'ponto_livres': ponto_livres,
        'ponto_ativos': ponto_ativos,
        'ramal_livres': ramal_livres,
        'senha_livres': senha_livres,
        'pontodados_modificados': pontodados_modificados,
        'pontovoz_modificados': pontovoz_modificados,
        'ramal_modificados': ramal_modificados,
        'senha_modificados': senha_modificados,
        'total_senha_d': total_senha_d,
        'total_service': total_service,
        'total_host': total_host,
        'total_ip': total_ip,
        'host_linux': host_linux,
        'host_win': host_win,
        'host_bsd': host_bsd,
        'host_other': host_other,
        'servicecategories': servicecategories,
        'ip_modificados': ip_modificados,
        'service_modificados': service_modificados,
        'host_modificados': host_modificados,
        'switch_modificados': switch_modificados,
        'phonecats': phonecats,
        'phonetypes': phonetypes,
        'total_printer': total_printer,
        'total_phone': total_phone,
        'user': usr,
        'title': title,
        'logs':logs,
        })

#    if not request.user.is_authenticated():
#        return HttpResponse("You are not logged in.")

#    else:
#        return HttpResponse(template.render(context))



@login_required(login_url='/ace/login/')
def config(request):
    # config = AceConfig.objects.get()
    try:
        config = AceConfig.objects.get()

    except AceConfig.DoesNotExist:
        config = ""

    title = "Configurações"

    return render ( request, 'config.html',
        {'title':title,
         'config':config,
        })




@login_required(login_url='/ace/login/')
@permission_required('ace.add_aceconfig', raise_exception=True)
def config_new(request):
    title = "Editar Configurações"
    if request.method == "POST":
        form = ConfigForm(request.POST)

        if form.is_valid():
            config = form.save()
            return redirect('config')
    else:
        form = ConfigForm()
        return render(request, 'forms/config_edit.html', {'form': form, 'title': title})


@login_required(login_url='/ace/login/')
@permission_required('ace.change_aceconfig', raise_exception=True)
def config_edit(request):
    user = request.user
    try:
        config = AceConfig.objects.get()

    except AceConfig.DoesNotExist:
        return redirect('config_new')

    title = "Editar Configurações"

    if request.method == "POST":
        form = ConfigForm(request.POST, instance=config)
        if form.is_valid():
            config = form.save()
            addlog("Config", "Config edit", datetime.datetime.today(), user, 'config', config.id)
            return redirect('config')
    else:
        form = ConfigForm(instance=config)
    return render(request, 'forms/config_edit.html', {'form': form, 'title': title})


@login_required(login_url='/ace/login/')
def switchlist(request):
    f = SwitchFilter(request.GET, queryset=Switch.objects.all())
    fc = f.qs.count()
    switch_total = Switch.objects.all().count()
    title = "Switches"

    try:
        config = AceConfig.objects.get()
        stacklist_results = config.stacklist_results

    except AceConfig.DoesNotExist:
        stacklist_results = "10"

    # tabela
    table = SwitchTable(f.qs)
    RequestConfig(request, paginate={'per_page': stacklist_results}).configure(table)      

    # export
    export_format = request.GET.get('_export', None)
    if TableExport.is_valid_format(export_format):
        exporter = TableExport(export_format, table)
        return exporter.response('table.{}'.format(export_format))       

    return render(request, 'switchlist.html',
                  {'table': table, 'filter': f, "total": switch_total, "title": title,
                   'fc': fc})


@login_required(login_url='/ace/login/')
def switchdetail(request, switch_id):
    try:
        switch = Switch.objects.get(pk=switch_id)
        history = switch.history.all()
        p = Switchport.objects.all().filter(switch=switch)

    except Switch.DoesNotExist:
        raise Http404

    return render(request, 'switchdetail.html', {'switch': switch, 'p': p, 'history':history })


@login_required(login_url='/ace/login/')
def vlanlist(request):
    vlans = Vlan.objects.all().order_by('vlanid')
    vlans_total = vlans.count()
    title = "VLANs"

    # modificação para django 1.11

    # tabela
    table = VlanTable(vlans)
    RequestConfig(request, paginate={'per_page': '10'}).configure(table)        

    return render(request, 'vlan_list.html',
                  {'table': table, "total": vlans_total, "title": title,
                   'vlans': vlans})        


@login_required(login_url='/ace/login/')
def vlandetail(request, vlan_id):
    title = "Vlan"
    try:
        vlan = Vlan.objects.get(pk=vlan_id)
        networks = Network.objects.filter(vln_id=vlan_id)
        # swports = Switchport.objects.filter(vlans__in=vlan)
        swports = vlan.switchport_set.all()

    except Vlan.DoesNotExist:
        raise Http404

    return render(request, 'vlandetail.html', {'vlan': vlan, 'networks': networks, 'swports': swports, 'title':title, })


@login_required(login_url='/ace/login/')
def patchpaneldetail(request, patchpanel_id):
    try:
        patchpanel = Patchpanel.objects.get(pk=patchpanel_id)
        p = Patchpanelport.objects.all().filter(patchpanel=patchpanel)

    except Patchpanel.DoesNotExist:
        raise Http404

    return render(request, 'patchpaneldetail.html', {'patchpanel': patchpanel, 'p': p, })


@login_required(login_url='/ace/login/')
def patchpanelport(request, patchpanelport_id):
    try:
        ppp = Patchpanelport.objects.get(pk=patchpanelport_id)
    except Patchpanelport.DoesNotExist:
        raise Http404

    return render(request, 'patchpanelport.html', {'patchpanelport': ppp, })


@login_required(login_url='/ace/login/')
def userdetail(request, user_id):
    try:
        usr = User.objects.get(pk=user_id)
        phones = Phone.objects.filter(user=usr)
        po = Phoneownership.objects.filter(user=usr)
        totalpo = po.count()
        phoneownership = po.order_by('-active')[:10]

    except User.DoesNotExist:
        raise Http404

    return render(request, 'userdetail.html', {'usr': usr, 'phones': phones, 'phoneownership': phoneownership, 'totalpo':totalpo,  })


@login_required(login_url='/ace/login/')
def userlist(request):
    # userlist = User.objects.order_by('username')
    f = UserFilter(request.GET, queryset=User.objects.all())
    fc = f.qs.count()
    user_total = User.objects.all().count()
    title = "Usuários"    

    try:
        config = AceConfig.objects.get()
        userlist_results = config.userlist_results

    except AceConfig.DoesNotExist:
        userlist_results = "10"

    # tabela
    table = UserTable(f.qs)
    RequestConfig(request, paginate={'per_page': userlist_results}).configure(table)      

    # export
    export_format = request.GET.get('_export', None)
    if TableExport.is_valid_format(export_format):
        exporter = TableExport(export_format, table)
        return exporter.response('table.{}'.format(export_format))       

    
    return render(request, 'user_list.html',
                  {'filter': f, "total": user_total, "title": title, 'fc': fc, "userlist_results": userlist_results, 'table':table})



@login_required(login_url='/ace/login/')
def owneriddetail(request, ownerid_id):
    try:
        ownerid = Ownerid.objects.get(pk=ownerid_id)
        devices = Device.objects.filter(ownerid=ownerid)

    except Ownerid.DoesNotExist:
        raise Http404

    return render(request, 'owneriddetail.html', {'ownerid': ownerid, 'devices': devices})


@login_required(login_url='/ace/login/')
def owneridlist(request):
    f = OwneridFilter(request.GET, queryset=Ownerid.objects.all())
    total = Ownerid.objects.all().count()
    # config = AceConfig.objects.get()
    # owneridlist_results = config.owneridlist_results
    title = u"Patrimônios"

    try:
        config = AceConfig.objects.get()
        owneridlist_results = config.owneridlist_results

    except AceConfig.DoesNotExist:
        owneridlist_results = "10"

    return render(request, 'ownerid_list.html',
                  {'filter': f, "total": total, "title": title, 'owneridlist_results': owneridlist_results})


@login_required(login_url='/ace/login/')
def swport(request, portaswitch_id):
    try:
        portaswitch = Switchport.objects.get(pk=portaswitch_id)
        vlans = portaswitch.vlans.all()
        h = portaswitch.host
        if vlans.count() > 1:
            trunk = "OK"
        else:
            trunk = "NOK"
        if h:
            device = Device.objects.get(id=h.id)

            # testa host
            try:
                host = Host.objects.get(device_ptr_id=device.id)
                if host:
                    t = "host"
            except:
                pass
            
            try:
                switch = Switch.objects.get(device_ptr_id=device.id)
                if switch:
                    t = "switch"
            except:
                pass

            try:
                stack = Stack.objects.get(device_ptr_id=device.id)
                if stack:
                    t = "stack"
            except:
                pass

            try:
                printer = Printer.objects.get(device_ptr_id=device.id)
                if printer:
                    t = "printer"
            except:
                pass                

        else:
            t = ""

        # vlan = subprocess.check_output(['aux/snmpport.sh', portaswitch.num])
    except Switchport.DoesNotExist:
        raise Http404

    return render(request, 'switchport.html', {'portaswitch': portaswitch, 'vlans': vlans, 'trunk': trunk, 't':t})


@login_required(login_url='/ace/login/')
def netpointlist(request):
    f = NetpointFilter(request.GET, queryset=Netpoint.objects.all())
    fc = f.qs.count()
    free = Netpoint.objects.filter(pointtype='desativado').order_by('num')
    netpoint_total = Netpoint.objects.all().count()


    try:
        config = AceConfig.objects.get()
        netpointlist_results = config.netpointlist_results

    except AceConfig.DoesNotExist:
        netpointlist_results = "10"

    title = "Pontos de rede"

    # tabela
    table = NetpointTable(f.qs)
    RequestConfig(request, paginate={'per_page': netpointlist_results}).configure(table)

    # export
    export_format = request.GET.get('_export', None)
    if TableExport.is_valid_format(export_format):
        exporter = TableExport(export_format, table)
        return exporter.response('table.{}'.format(export_format))

    return render(request, 'pointlist.html',
                  {'netpointlist_results': netpointlist_results, 'filter': f, "total": netpoint_total, "title": title,
                   'fc': fc, 'free': free, 'table': table })





@login_required(login_url='/ace/login/')
def pointdetail(request, ponto_id):
    try:
        ponto = Netpoint.objects.get(pk=ponto_id)

    except Netpoint.DoesNotExist:
        raise Http404

    return render(request, 'pointdetail.html', {'ponto': ponto, })


@login_required(login_url='/ace/login/')
def phonelist(request):
    user = request.user
    phones = Phone.objects.filter(password=False)
    f = PhoneFilter(request.GET, queryset=phones)
    fc = f.qs.count()
    total = phones.count()
    title = "Telefones"  

    try:
        config = AceConfig.objects.get()
        phonelist_results = config.phonelist_results

    except AceConfig.DoesNotExist:
        phonelist_results = "10"

    # tabela
    table = PhoneTable(f.qs)
    RequestConfig(request, paginate={'per_page': phonelist_results}).configure(table)

    # export
    export_format = request.GET.get('_export', None)
    if TableExport.is_valid_format(export_format):
        exporter = TableExport(export_format, table)
        return exporter.response('table.{}'.format(export_format))        

    return render(request, 'phonelist.html',
                  {'filter': f, "total": total, "title": title, 'fc': fc, 'table':table, })


@login_required(login_url='/ace/login/')
def passwordlist(request):
    user = request.user
    passwords = Phone.objects.filter(password=True)
    f = PasswordFilter(request.GET, queryset=passwords)
    fc = f.qs.count()
    total = passwords.count()
    title = "Senhas para chamadas"
    

    try:
        config = AceConfig.objects.get()
        passwordlist_results = config.passwordlist_results

    except AceConfig.DoesNotExist:
        passwordlist_results = "10"

    #if user.has_perm('ace.view_password') or user.is_superuser:
    # tabela
    table = PasswordTable(f.qs)
    RequestConfig(request, paginate={'per_page': passwordlist_results}).configure(table)

    # export
    export_format = request.GET.get('_export', None)
    if TableExport.is_valid_format(export_format):
        exporter = TableExport(export_format, table)
        return exporter.response('table.{}'.format(export_format))        

    return render(request, 'phonelist.html',
                  {'filter': f, "total": total, "title": title, 'fc': fc, 'table':table, 'passwords':passwords,  })



@login_required(login_url='/ace/login/')
def phoneassociation(request):
    user = request.user
    po = Phoneownership.objects.filter(phone__password=False).order_by('-date_activation', '-date_deactivation')
    f = PhoneAssociationFilter(request.GET, queryset=po)
    fc = f.qs.count()
    total = po.count()
    title = "Associações de usuário a telefone"
    object_type = "phone"

    # tabela
    table = PhoneAssociationTable(f.qs)
    RequestConfig(request, paginate={'per_page': 15}).configure(table)

    # export
    export_format = request.GET.get('_export', None)
    if TableExport.is_valid_format(export_format):
        exporter = TableExport(export_format, table)
        return exporter.response('table.{}'.format(export_format))

    return render(request, 'phoneassociation-list.html',
                  {'filter': f, "total": total, "title": title, 'fc': fc, 'table': table, 'object_type':object_type })


@login_required(login_url='/ace/login/')
def passwordassociation(request):
    user = request.user
    po = Phoneownership.objects.filter(phone__password=True).order_by('-date_activation', '-date_deactivation')
    f = PasswordAssociationFilter(request.GET, queryset=po)
    fc = f.qs.count()
    total = po.count()
    title = "Associações de usuário a senhas"
    object_type = "password"

    # tabela
    table = PasswordAssociationTable(f.qs)
    RequestConfig(request, paginate={'per_page': 15}).configure(table)

    # export
    export_format = request.GET.get('_export', None)
    if TableExport.is_valid_format(export_format):
        exporter = TableExport(export_format, table)
        return exporter.response('table.{}'.format(export_format))

    return render(request, 'phoneassociation-list.html',
                  {'filter': f, "total": total, "title": title, 'fc': fc, 'table': table, 'object_type':object_type })



@login_required(login_url='/ace/login/')
#@permission_required('ace.change_phone', raise_exception=True)
def phonedetail(request, phone_id):
    title = "Telefone/Senha"
    try:
        ramal = Phone.objects.get(pk=phone_id)
        phoneownership = Phoneownership.objects.filter(phone=ramal).order_by('-date_activation')
        history = ramal.history.first()
        if phoneownership:
            poactive = phoneownership.filter(active=True)
        else:
            poactive = ""

    except Phone.DoesNotExist:
        raise Http404

    try:
        ponto = Netpoint.objects.get(phone=ramal.id)
    except Netpoint.DoesNotExist:
        ponto = ""

    return render(request, 'phonedetail.html',
                  {'ramal': ramal, 'ponto': ponto, 'phoneownership': phoneownership, 'poactive': poactive,
                   'history': history, 'title': title})


# locais
@login_required(login_url='/ace/login/')
def placelist(request):
    f = PlaceFilter(request.GET, queryset=Place.objects.all())
    fc = f.qs.count()
    place_total = Place.objects.all().count()

    try:
        config = AceConfig.objects.get()
        placelist_results = config.placelist_results

    except AceConfig.DoesNotExist:
        placelist_results = "10"

    title = "Locais"

    # tabela
    table = PlaceTable(f.qs)
    RequestConfig(request, paginate={'per_page': placelist_results}).configure(table)     

    return render(request, 'placelist.html',
                  {'table': table,'filter': f, "total": place_total, "title": title, 'fc': fc, })







@login_required(login_url='/ace/login/')
def sectorlist(request):
    f = SectorFilter(request.GET, queryset=Sector.objects.all())
    fc = f.qs.count()
    sector_total = Sector.objects.all().count()
    # config = AceConfig.objects.get()
    # sectorlist_results = config.sectorlist_results
    title = "Setores/Departamentos"

    try:
        config = AceConfig.objects.get()
        sectorlist_results = config.sectorlist_results

    except AceConfig.DoesNotExist:
        sectorlist_results = "10"

    # tabela
    table = SectorTable(f.qs)
    RequestConfig(request, paginate={'per_page': sectorlist_results}).configure(table)             

    return render(request, 'sector_list.html',
                  {'filter': f, "total": sector_total, "title": title,
                   'fc': fc, 'table': table,})


@login_required(login_url='/ace/login/')
def placedetail(request, place_id):
    title = "Local"
    try:
        local = Place.objects.get(pk=place_id)
        p = Netpoint.objects.filter(place=local)
        ptotal = p.count()
        # pd = local.Netpoint_set.all().filter(pointtype='dados').count()
        pd = Netpoint.objects.all().filter(place=local, pointtype='dados').count()
        pv = Netpoint.objects.all().filter(place=local, pointtype='voz').count()
        pvoip = Netpoint.objects.all().filter(place=local, pointtype='voip').count()
        pdesat = Netpoint.objects.all().filter(place=local, pointtype='desativado').count()
        phone = Phone.objects.all().filter(place=local, active=True)
        phonetotal = phone.count()
        h = local.host_set.all()

    except Place.DoesNotExist:
        raise Http404
    return render(request, 'placedetail.html',
                  {'local': local, 'p': p, 'pd': pd, 'pv': pv, 'pvoip': pvoip, 'pdesat': pdesat, 'phone': phone,
                   'ptotal': ptotal, 'phonetotal': phonetotal, 'title': title, 'h':h})


@login_required(login_url='/ace/login/')
def sectordetail(request, sector_id):
    try:
        sector = Sector.objects.get(pk=sector_id)
        places = Place.objects.filter(sector=sector)

    except Sector.DoesNotExist:
        raise Http404
    return render(request, 'sectordetail.html', {'sector': sector, 'places': places})


@login_required(login_url='/ace/login/')
def stacklist(request):
    f = StackFilter(request.GET, queryset=Stack.objects.all())
    fc = f.qs.count()
    total = Stack.objects.all().count()
    title = u"Pilhas"

    try:
        config = AceConfig.objects.get()
        stacklist_results = config.stacklist_results

    except AceConfig.DoesNotExist:
        stacklist_results = "10"

    # tabela
    table = StackTable(f.qs)
    RequestConfig(request, paginate={'per_page': stacklist_results}).configure(table)   

    # export
    export_format = request.GET.get('_export', None)
    if TableExport.is_valid_format(export_format):
        exporter = TableExport(export_format, table)
        return exporter.response('table.{}'.format(export_format))

    return render(request, 'stack_list.html',
                  {'table': table, 'filter': f, "total": total, "title": title, 'fc': fc})


@login_required(login_url='/ace/login/')
@permission_required('ace.add_stack', raise_exception=True)
def stackdetail(request, pilha_id):
    try:
        pilha = Stack.objects.get(pk=pilha_id)
        s = Switch.objects.all().filter(stack_field=pilha)
        i = Ip.objects.all().filter(device=pilha_id)

    except Stack.DoesNotExist:
        raise Http404

    return render(request, 'stackdetail.html', {'pilha': pilha, 's': s, 'i': i})


@login_required(login_url='/ace/login/')
def racklist(request):
    f = RackFilter(request.GET, queryset=Rack.objects.all())
    fc = f.qs.count()
    total = Rack.objects.all().count()
    # config = AceConfig.objects.get()
    # racklist_results = config.racklist_results
    title = "Racks"

    try:
        config = AceConfig.objects.get()
        racklist_results = config.racklist_results

    except AceConfig.DoesNotExist:
        racklist_results = "10"

    # tabela
    table = RackTable(f.qs)
    RequestConfig(request, paginate={'per_page': racklist_results }).configure(table)            

    # export
    export_format = request.GET.get('_export', None)
    if TableExport.is_valid_format(export_format):
        exporter = TableExport(export_format, table)
        return exporter.response('table.{}'.format(export_format))           

    return render(request, 'rack_list.html',
                  {'filter': f, "total": total, "title": title, 'fc': fc, 'table': table})






@login_required(login_url='/ace/login/')
def patchpanellist(request):
    f = PatchpanelFilter(request.GET, queryset=Patchpanel.objects.all())
    fc = f.qs.count()
    total = Patchpanel.objects.all().count()
    title = "Patchpanels"

    try:
        config = AceConfig.objects.get()
        patchpanellist_results = config.patchpanel_results

    except AceConfig.DoesNotExist:
        patchpanellist_results = "10"

    # tabela
    table = PatchpanelTable(f.qs)
    RequestConfig(request, paginate={'per_page': patchpanellist_results }).configure(table)            

    # export
    export_format = request.GET.get('_export', None)
    if TableExport.is_valid_format(export_format):
        exporter = TableExport(export_format, table)
        return exporter.response('table.{}'.format(export_format))          

    return render(request, 'patchpanel_list.html',
                  { 'filter': f, "total": total, "title": title,
                   'fc': fc, 'table': table})


@login_required(login_url='/ace/login/')
def rackdetail(request, rack_id):
    title = "Detalhe do rack"
    try:
        rack = Rack.objects.get(pk=rack_id)
        s = Switch.objects.all().filter(rack=rack)
        p = Patchpanel.objects.all().filter(rack=rack)
        points = Netpoint.objects.filter(rack=rack)

    except Rack.DoesNotExist:
        raise Http404

    return render(request, 'rackdetail.html', {'rack': rack, 's': s, 'p': p, 'points': points, 'title':title})


# hosts
@login_required(login_url='/ace/login/')
def hostlist(request):
    title = "Equipamentos (Hosts)"

    # config
    try:
        config = AceConfig.objects.get()
        hostlist_results = config.hostlist_results
    except AceConfig.DoesNotExist:
        hostlist_results = "10"

    hosts = Host.objects.all()
    host_total = hosts.count()
    f = HostFilter(request.GET, queryset=hosts)
    fc = f.qs.count()

    # tabela
    table = HostTable(f.qs)
    RequestConfig(request, paginate={'per_page': hostlist_results}).configure(table)

    # export
    export_format = request.GET.get('_export', None)
    if TableExport.is_valid_format(export_format):
        exporter = TableExport(export_format, table)
        return exporter.response('table.{}'.format(export_format))

    return render(request, 'host_list.html',
                  {"total": host_total, "title": title, 'fc': fc, 'filter': f, 'hostlist_results': hostlist_results,
                   'table': table})


# impressoras
@login_required(login_url='/ace/login/')
def printerlist(request):
    title = "Impressoras/Scanners"

    # config
    try:
        config = AceConfig.objects.get()
        printerlist_results = config.printerlist_results

    except AceConfig.DoesNotExist:
        printerlist_results = "10"

    printers = Printer.objects.all()
    printer_total = printers.count()
    f = PrinterFilter(request.GET, queryset=printers)
    fc = f.qs.count()
    t = "printer"

    # tabela
    table = PrinterTable(f.qs)
    RequestConfig(request, paginate={'per_page': printerlist_results}).configure(table)

    # export
    export_format = request.GET.get('_export', None)
    if TableExport.is_valid_format(export_format):
        exporter = TableExport(export_format, table)
        return exporter.response('table.{}'.format(export_format))

    return render(request, 'host_list.html', {"total": printer_total, "title": title, 'fc': fc, 'filter': f,
                                              'hostlist_results': printerlist_results, 't': t, 'table': table})


@login_required(login_url='/ace/login/')
def servicelist(request):
    f = ServiceFilter(request.GET, queryset=Service.objects.all())
    fc = f.qs.count()
    service_total = Service.objects.all().count()
    # servicelist_results = config.servicelist_results
    title = "Serviços"

    # config
    try:
        config = AceConfig.objects.get()
        servicelist_results = config.servicelist_results

    except AceConfig.DoesNotExist:
        servicelist_results = "10"    

    # tabela
    table = ServiceTable(f.qs)
    RequestConfig(request, paginate={'per_page': servicelist_results }).configure(table)    

    # export
    #export_format = request.GET.get('_export', None)    

    #if TableExport.is_valid_format(export_format):
    #    exporter = TableExport(export_format, table)
    #    return exporter.response('table.{}'.format(export_format))    


    return render(request, 'service_list.html',
                  {'table': table, 'filter': f, "total": service_total, "title": title,
                   'fc': fc})

    
    
    
    




@login_required(login_url='/ace/login/')
def hostdetail(request, host_id):
    title = "Equipamento"
    try:
        host = Host.objects.get(pk=host_id)
        history = host.history.all()
        swport = Switchport.objects.filter(host=host_id)
        i = Ip.objects.filter(device=host_id)
        u = host.hostupdate_set.all()
        # u = host.hostupdate_set.all().order_by('aplication_date')
        #s = Service.objects.filter(ip=i)
        s = Service.objects.filter(ip__in=i)
        n = []

        for swp in swport:
            try:
                netpoint = Netpoint.objects.get(swport=swp)
                if netpoint:
                    n.append(netpoint)
            except:
                pass


    #        login = host.admuser
    #        server = host.name
    #        pw = host.admpass
    #        if host.osplatform != 'windows':
    #            try:
    #                #output1 = subprocess.check_output(['fab', '--fabfile=fabfile.py', 'mem', '--hosts=andes.prdf.mpf.gov.br', '--user=root', '--password=t1hu4n4!@#','--hide=status,running,warnings'])
    #                memoria = subprocess.check_output(['fab', '-f', 'fabfile.py', 'mem', '-H', server, '-u', login, '-p', pw,'--hide=status,running,warnings', '--timeout=2', '--abort-on-prompts'])
    #                proc = subprocess.check_output(['fab', '-f', 'fabfile.py', 'cpu', '-H', server, '-u', login, '-p', pw,'--hide=status,running,warnings', '--timeout=2', '--abort-on-prompts'])
    #                #output1 = output0.split()
    #                #output = output1[2::3]
    #                ram=int(filter(str.isdigit, memoria))
    #                cpu=int(filter(str.isdigit, proc))

    #                erro = ""
    #            except subprocess.CalledProcessError:
    #                erro = "erro"
    #                ram = "sem informaçṍes"
    #                cpu = "sem informaçṍes"
    #        else:
    #            erro = ""
    #            ram  = ""
    #            cpu = ""

    except Host.DoesNotExist:
        raise Http404

    return render(request, 'hostdetail.html',
                  {'host': host, 's': s, 'i': i, 'swport': swport, 'n': n, 'u': u, 'title': title, 'history':history})


@login_required(login_url='/ace/login/')
def printerdetail(request, printer_id):
    try:
        host = Printer.objects.get(pk=printer_id)
        history = host.history.all()
        title = "Impressora"
        t = "printer"
        i = Ip.objects.all().filter(device=printer_id)

    except Printer.DoesNotExist:
        raise Http404    

    return render(request, 'hostdetail.html', {'host': host, 't': t, 'i': i, 'title': title, 'history':history})


@login_required(login_url='/ace/login/')
def servicedetail(request, service_id):
    try:
        service = Service.objects.get(pk=service_id)
        categories = service.category.all()
    except Service.DoesNotExist:
        raise Http404

    return render(request, 'servicedetail.html', {'service': service, 'categories': categories})


@login_required(login_url='/ace/login/')
def servicecatdetail(request, servicecategory_id):
    try:
        servicecat = Servicecategory.objects.get(pk=servicecategory_id)
        s = Service.objects.all().filter(category=servicecat)
    except Servicecategory.DoesNotExist:
        raise Http404

    return render(request, 'servicecatdetail.html', {'servicecat': servicecat, 's': s})


@login_required(login_url='/ace/login/')
def iplist(request):
    f = IpFilter(request.GET, queryset=Ip.objects.all())
    fc = f.qs.count()
    total = Ip.objects.all().count()
    title = u"Endereços IP"

    try:
        config = AceConfig.objects.get()
        iplist_results = config.iplist_results

    except AceConfig.DoesNotExist:
        iplist_results = "10"

    # tabela
    table = IpTable(f.qs)
    RequestConfig(request, paginate={'per_page': iplist_results}).configure(table)            

    # export
    export_format = request.GET.get('_export', None)
    if TableExport.is_valid_format(export_format):
        exporter = TableExport(export_format, table)
        return exporter.response('table.{}'.format(export_format))    

    return render(request, 'ip_list.html',
                  {'filter': f, "total": total, "title": title, 'fc': fc, 'table': table})






@login_required(login_url='/ace/login/')
def ipdetail(request, ip_id):
    try:
        ip = Ip.objects.get(pk=ip_id)

    except Ip.DoesNotExist:
        raise Http404

    try:
        s = Service.objects.filter(ip=ip)

    except Service.DoesNotExist:
        s = ""

    return render(request, 'ipdetail.html', {'ip': ip, 's': s})


@login_required(login_url='/ace/login/')
def networklist(request):
    f = NetworkFilter(request.GET, queryset=Network.objects.all())
    fc = f.qs.count()
    total = Network.objects.all().count()
    title = u"Redes"

    try:
        config = AceConfig.objects.get()
        networklist_results = config.networklist_results

    except AceConfig.DoesNotExist:
        networklist_results = "10"

    # tabela
    table = NetworkTable(f.qs)
    RequestConfig(request, paginate={'per_page': networklist_results }).configure(table)            

    # export
    export_format = request.GET.get('_export', None)
    if TableExport.is_valid_format(export_format):
        exporter = TableExport(export_format, table)
        return exporter.response('table.{}'.format(export_format))           

    return render(request, 'network_list.html',
                  {'filter': f, "total": total, "title": title, 'fc': fc, 'table': table})


@login_required(login_url='/ace/login/')
def manufactorerdetail(request, manufactorer_id):
    try:
        manufactorer = Manufctorer.objects.get(pk=manufactorer_id)

    except Manufactorer.DoesNotExist:
        raise Http404

    try:
        s = Device.objects.filter(Manufactorer=Manufactorer)

    except Device.DoesNotExist:
        s = ""

    return render(request, 'manufactorerdetail.html', {'manufactorer': manufactorer, 's': s})


@login_required(login_url='/ace/login/')
def manufactorerlist(request):
    manufactorer_list = Manufactorer.objects.order_by('name')
    manufactorer_total = Manufactorer.objects.all().count
    template = loader.get_template('manufactorer_list.html')
    context = RequestContext(request, {
        'manufactorer_list': manufactorer_list,
        'manufactorer_total': manufactorer_total,
    })

    return HttpResponse(template.render(context))


def findips(start, end):
    start = ip_address(start)
    end = ip_address(end)
    result = []
    while start <= end:
        result.append(str(start))
        start += 1
    return result


@login_required(login_url='/ace/login/')
def networkdetail(request, rede_id):
    ltotal = []
    lips = []
    try:
        network = Network.objects.get(pk=rede_id)
        r = network.address
        m = str(network.mask)
        # rede + mascara ex: 192.168.0.0/24
        rm = r + "/" + m
        # ips fixos
        i = Ip.objects.filter(network=network)
        # total de ips da rede
        qf = i.count()
        # lista de todos os objetos ipaddress da rede
        total = list(ipaddress.ip_network(rm).hosts())

        rede = ipaddress.ip_network(rm)
        broadcast = rede.broadcast_address

        # total de ips da rede
        for k in total:
            ltotal.append(str(k))


        for j in i:
            lips.append(j.address)

        # qtotal = len(list(ipaddress.ip_network(rm).hosts()))

        # quantidade de ips da rede
        qtotal = len(total)
        dhcp = network.dhcp

        if dhcp:
            start = re.split(r'(\.|/)', network.dhcp_start)
            end = re.split(r'(\.|/)', network.dhcp_end)
            # primeiro ip dhcp
            ipstart = int(start[-1])
            # ultimo ip dhcp
            ipend = int(end[-1])
            # quantidade de ips do dhcp
            qdhcp = len(range(ipstart, ipend + 1))
            d = qtotal - qdhcp - qf
            dhcprange = findips(network.dhcp_start, network.dhcp_end)

            free = list(set(ltotal) - set(lips) - set(dhcprange))
            free.sort()


        else:

            d = qtotal - qf
            free = list(set(ltotal) - set(lips))
            qdhcp = ""

        # tabela
        table = IpTable(i)
        RequestConfig(request, paginate={'per_page': 15 }).configure(table)

        # export
        export_format = request.GET.get('_export', None)
        if TableExport.is_valid_format(export_format):
            exporter = TableExport(export_format, table)
            return exporter.response('table.{}'.format(export_format))


    except Network.DoesNotExist:
        raise Http404
    return render(request, 'networkdetail.html',
                  {'network': network, 'i': i, 'd': d, 'free': free, 'qdhcp': qdhcp, 'broadcast': broadcast, 'qf':qf, 'table':table})


def user_login(request):
    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        username = request.POST['username']
        password = request.POST['password']

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect('/ace')
            else:
                # An inactive account was used - no logging in!
                # return HttpResponse("Sua conta foi desabilitada.")
                return render(request, 'login_error.html', {})
        else:
            # Bad login details were provided. So we can't log the user in.
            # print "Credenciais invalidas: {0}, {1}".format(username, password)
            # return HttpResponse("Credenciais invalidas.")
            return render(request, 'login_error.html', {})

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render(request, 'login.html', {})
        # return render(request, 'login.html', {'systitle': systitle})


@login_required(login_url='/ace/login/')
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/ace/login')


def search(request):
    error = False
    if 's' in request.GET:
        busca = 's'
        q = request.GET['s']
        if not q:
            error = True
            pontos = []
            locais = []
            ramais = []
            hosts = []
            switchs = []
            stacks = []
            services = []
            ips = []
            passwords = []
            ownerids = []
            users = []
            phonetypes = []
            phonecat = []
            networks = []
        else:
            pontos = Netpoint.objects.filter(num__icontains=q)
            locais = Place.objects.filter(name__icontains=q)
            ramais = []
            phones = Phone.objects.filter(password=False,num__icontains=q)
            phonetypes = Phone.objects.filter(telephonetype__name__icontains=q)
            phonecat = Phone.objects.filter(phonecategory__name__icontains=q)
            ramais = list(chain(phonetypes, phonecat, phones))
            hosts = Host.objects.filter(name__icontains=q)
            switchs = Switch.objects.filter(name__icontains=q)
            stacks = Stack.objects.filter(name__icontains=q)
            services = Service.objects.filter(name__icontains=q)
            ips = Ip.objects.filter(address__icontains=q)
            networks = Network.objects.filter(name__icontains=q)
            ownerids = Ownerid.objects.filter(num__icontains=q)
            userslogin = User.objects.filter(username__icontains=q)
            usersfname = User.objects.filter(first_name__icontains=q)
            userslname = User.objects.filter(last_name__icontains=q)
            userlist = list(chain(userslogin, usersfname, userslname))
            users = list(set(userlist))

        return render(request, 'search_results.html',

                      {'pontos': pontos, 'locais': locais, 'ramais': ramais, 'hosts': hosts, 'switchs': switchs,
                       'stacks': stacks, 'services': services, 'ips': ips, 'ownerids': ownerids, 'users': users,
                       'networks': networks, 'query': q, 'busca': busca, 'error': error})


""" formularios host """


@login_required(login_url='/ace/login/')
@permission_required('ace.add_host', raise_exception=True)
def host_new(request):
    title = "Cria&ccedil;&atilde;o/Ediç&atilde;o de Host/Equipamento"
    if request.method == "POST":
        user = request.user
        form = HostForm(request.POST)
        

        try:
            config = AceConfig.objects.get()
            default_host_group = config.default_host_group

        except AceConfig.DoesNotExist:
            config = ""
            default_host_group = ""

        if form.is_valid():
            host = form.save()
            host.save()
            #cria log
            addlog(host.name, "host creation", host.modification_date, user, "host", host.id)
            if default_host_group:
                host.groups.add(default_host_group.id)
            return redirect('hostdetail', host.id)
        else:
            return render(request, 'forms/host_edit.html', {'form': form, 'title':title})

    else:
        form = HostForm()
        return render(request, 'forms/host_edit.html', {'form': form, 'title':title})


# testes json ajax form
@login_required(login_url='/ace/login/')
@permission_required('ace.add_host', raise_exception=True)
def host_create(request):
    title = "Cria&ccedil;&atilde;o/Ediç&atilde;o de Host/Equipamento"
    data = dict()

    if request.method == "POST":
        user = request.user
        form = HostForm(request.POST)

        try:
            config = AceConfig.objects.get()
            default_host_group = config.default_host_group

        except AceConfig.DoesNotExist:
            config = ""
            default_host_group = ""

        if form.is_valid():
            form.save()
            # host = form.save()
            data['form_is_valid'] = True
            # cria log
            # addlog(host.name, "host creation", host.modification_date, user, "host", host.id)
            if default_host_group:
                host.groups.add(default_host_group.id)
        else:
            data['form_is_valid'] = False

    else:
        form = HostForm()

    context = {'form': form}
    data['html_form'] = render_to_string('includes/partial_host_create.html',
                                         context,
                                         request=request
                                         )
    return JsonResponse(data)

    # return render(request, 'forms/host_edit.html', {'form': form, 'title':title})



@login_required(login_url='/ace/login/')
@permission_required('ace.change_host', raise_exception=True)
def host_edit(request, pk):
    host = get_object_or_404(Host, pk=pk)
    user = request.user
    title = "Cria&ccedil;&atilde;o/Ediç&atilde;o de Host/Equipamento"

    try:
        config = AceConfig.objects.get()
        default_host_group = config.default_host_group

    except AceConfig.DoesNotExist:
        config = ""
        default_host_group = ""

    # grupos do usuario logado
    user_group = user.groups.all()

    # grupos do host
    host_group = host.groups.all()

    # get objects present in both groups
    same_group = set(user_group).intersection(set(host_group))

    if same_group or user.is_superuser:

        if request.method == "POST":
            form = HostForm(request.POST, instance=host)
            if form.is_valid():
                host = form.save()
                host.save()
                #cria log
                addlog(host.name, "host edit", host.modification_date, user, "host", host.id)
                if default_host_group:
                    host.groups.add(default_host_group.id)                                
                return redirect('hostdetail', host.id)
            else:
                return render(request, 'forms/host_edit.html', {'form': form, 'title':title})

        else:
            form = HostForm(instance=host)
        return render(request, 'forms/host_edit.html', {'form': form, 'title':title})

    else:
        return render(request, '403.html')



@login_required(login_url='/ace/login/')
@permission_required('ace.delete_host', raise_exception=True)
def host_delete(request, pk, template_name='host_confirm_delete.html'):
    host = get_object_or_404(Host, pk=pk)
    ips = Ip.objects.filter(device_id=pk)
    title = "Exclus&atilde;o Host/Equipamento"
    user = request.user

    # grupos do usuario logado
    user_group = user.groups.all()

    # grupos do host
    host_group = host.groups.all()

    # get objects present in both groups
    same_group = set(user_group).intersection(set(host_group))

    if same_group or user.is_superuser:

        if ips:
            template = 'delete_error.html'
            return render(request, template, {'obj': host, 'itens': ips})

        if request.method == 'POST':
            host.delete()
            #cria log
            addlog(host.name, "host delete", datetime.datetime.today(), user, "host", host.id)
            return redirect('hostlist')
        return render(request, template_name, {'host': host, 'title': title})
    else:
        return render(request, '403.html')


""" formularios printer """


@login_required(login_url='/ace/login/')
@permission_required('ace.add_printer', raise_exception=True)
def printer_new(request):
    title = "Cria&ccedil;&atilde;o/Ediç&atilde;o de Impressora"
    try:
        config = AceConfig.objects.get()
        default_printer_group = config.default_printer_group

    except AceConfig.DoesNotExist:
        config = ""
        default_printer_group = ""

    if request.method == "POST":
        form = PrinterForm(request.POST)
        user = request.user
        t = "printer"
        
        if form.is_valid():
            printer = form.save()
            printer.save()
            #cria log
            addlog(printer.name, "printer add", datetime.datetime.today(), user, "printer", printer.id)
            if default_printer_group:
                printer.groups.add(default_printer_group.id)            
            return redirect('printerdetail', printer.id)
        else:
            return render(request, 'forms/host_edit.html', {'form': form, 't': t, 'title':title})

    else:
        form = PrinterForm()
        t = "printer"
        return render(request, 'forms/host_edit.html', {'form': form, 't': t, 'title':title})


@login_required(login_url='/ace/login/')
@permission_required('ace.change_printer', raise_exception=True)
def printer_edit(request, pk):
    host = get_object_or_404(Printer, pk=pk)
    t = "printer"
    title = "Cria&ccedil;&atilde;o/Ediç&atilde;o de Impressora"
    user = request.user

    try:
        config = AceConfig.objects.get()
        default_printer_group = config.default_printer_group

    except AceConfig.DoesNotExist:
        config = ""
        default_printer_group = ""

    # grupos do usuario logado
    user_group = user.groups.all()

    # grupos do host
    host_group = host.groups.all()

    # get objects present in both groups
    same_group = set(user_group).intersection(set(host_group))

    if same_group or user.is_superuser:

        if request.method == "POST":
            form = PrinterForm(request.POST, instance=host)
            if form.is_valid():
                host = form.save()
                host.save()
                #cria log
                addlog(host.name, "printer edit", datetime.datetime.today(), user, "printer", host.id)
                if default_printer_group:
                    host.groups.add(default_printer_group.id)  
                return redirect('printerdetail', host.id)
            else:
                return render(request, 'forms/host_edit.html', {'form': form, 't': t, 'title':title})

        else:
            form = PrinterForm(instance=host)
        return render(request, 'forms/host_edit.html', {'form': form, 't': t, 'title':title})

    else:
        return render(request, '403.html')



@login_required(login_url='/ace/login/')
@permission_required('ace.delete_printer', raise_exception=True)
def printer_delete(request, pk, template_name='host_confirm_delete.html'):
    printer = get_object_or_404(Printer, pk=pk)
    ips = Ip.objects.filter(device_id=pk)
    t = "printer"
    title = "Exclus&atilde;o Host/Equipamento"
    user = request.user

    # grupos do usuario logado
    user_group = user.groups.all()

    # grupos do host
    host_group = printer.groups.all()

    # get objects present in both groups
    same_group = set(user_group).intersection(set(host_group))

    if same_group or user.is_superuser:

        if ips:
            template = 'delete_error.html'
            return render(request, template, {'obj': printer, 'itens': ips})

        if request.method == 'POST':
            printer.delete()
            #cria log
            addlog(printer.name, "printer delete", datetime.datetime.today(), user, "printer", printer.id)
            return redirect('printerlist')
        return render(request, template_name, {'host': printer, 't': t, 'title': title})
    else:
        return render(request, '403.html')


""" formularios service """


@login_required(login_url='/ace/login/')
@permission_required('ace.add_service', raise_exception=True)
def service_new(request):
    user = request.user
    if request.method == "POST":
        form = ServiceForm(request.POST)
        
        if form.is_valid():
            service = form.save(commit=True)
            service.save()
            #cria log
            #addlog(service.name, "service add", datetime.datetime.today(), user, service.id)
            return redirect('servicedetail', service.id)
        else:
            return render(request, 'forms/service_edit.html', {'form': form})
    else:
        form = ServiceForm()
        return render(request, 'forms/service_edit.html', {'form': form})


@login_required(login_url='/ace/login/')
@permission_required('ace.change_service', raise_exception=True)
def service_edit(request, pk):
    service = get_object_or_404(Service, pk=pk)
    user = request.user
    if request.method == "POST":
        form = ServiceForm(request.POST, instance=service)
        if form.is_valid():
            service = form.save()
            service.save()
            #cria log
            #addlog(service.name, "service edit", datetime.datetime.today(), user)
            return redirect('servicedetail', service.id)
        else:
            return render(request, 'forms/service_edit.html', {'form': form})

    else:
        form = ServiceForm(instance=service)
    return render(request, 'forms/service_edit.html', {'form': form})


@login_required(login_url='/ace/login/')
@permission_required('ace.delete_service', raise_exception=True)
def service_delete(request, pk, template_name='service_confirm_delete.html'):
    service = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        service.delete()
        return redirect('servicelist')
    return render(request, template_name, {'service': service})


""" formularios network """


@login_required(login_url='/ace/login/')
@permission_required('ace.add_network', raise_exception=True)
def network_new(request):
    user = request.user
    if request.method == "POST":
        form = NetworkForm(request.POST)

        if form.is_valid():
            network = form.save(commit=True)
            network.save()
            #cria log
            addlog(network.name, "network add", datetime.datetime.today(), user, "network", network.id)
            return redirect('networkdetail', network.id)
        else:
            return render(request, 'forms/network_edit.html', {'form': form})
    else:
        form = NetworkForm()
        return render(request, 'forms/network_edit.html', {'form': form})


@login_required(login_url='/ace/login/')
@permission_required('ace.change_network', raise_exception=True)
def network_edit(request, pk):
    user = request.user
    network = get_object_or_404(Network, pk=pk)
    if request.method == "POST":
        form = NetworkForm(request.POST, instance=network)
        if form.is_valid():
            network = form.save(commit=False)
            network.save()
            #cria log
            addlog(network.name, "network edit", datetime.datetime.today(), user, "network", network.id)
            return redirect('networkdetail', network.id)
        else:
            return render(request, 'forms/network_edit.html', {'form': form})

    else:
        form = NetworkForm(instance=network)
    return render(request, 'forms/network_edit.html', {'form': form})


@login_required(login_url='/ace/login/')
@permission_required('ace.delete_network', raise_exception=True)
def network_delete(request, pk, template_name='network_confirm_delete.html'):
    user = request.user
    network = get_object_or_404(Network, pk=pk)
    ips = Ip.objects.filter(network_id=pk)
    services = Service.objects.filter(network_id=pk)
    itens = list(chain(ips, services))

    if itens:
        template = 'delete_error.html'
        return render(request, template, {'obj': network, 'itens': itens})

    if request.method == 'POST':
        network.delete()
        #cria log
        addlog(network.name, "network delete", datetime.datetime.today(), user, "network", networks.id)
        return redirect('networklist')
    return render(request, template_name, {'network': network})


""" formularios IP """


@login_required(login_url='/ace/login/')
@permission_required('ace.add_ip', raise_exception=True)
def ip_new(request):
    user = request.user
    if request.method == "POST":
        form = IpForm(request.POST)

        if form.is_valid():
            ip = form.save(commit=True)
            ip.save()
            #cria log
            addlog(ip, "IP add", datetime.datetime.today(), user, "ip", ip.id)
            return redirect('ipdetail', ip.id)
        else:
            return render(request, 'forms/ip_edit.html', {'form': form})
    else:
        form = IpForm()
        return render(request, 'forms/ip_edit.html', {'form': form})

#Adiciona IP já na tela da rede
@login_required(login_url='/ace/login/')
@permission_required('ace.add_ip', raise_exception=True)
# def ip_new(request):
def ip_new2(request, pk, ipaddr):
    user = request.user
    ipaddr = ipaddr
    n = Network.objects.filter(pk=pk)
    title = "IP"

    if request.method == "POST":
        # print Network.objects.get(pk=pk)
        # form = IpFormnew(request.POST)

        updated_data = request.POST.copy()
        d = updated_data['device']
        t = updated_data['csrfmiddlewaretoken']
        c = updated_data['comments']
        # newdata = QueryDict('device=d&csrfmiddlewaretoken=t&network=network&comments=c&address=ipaddr')
        newdata = QueryDict(mutable=True)
        newdata.update({'device': d, 'csrfmiddlewaretoken': t, 'network': n, 'comments': c, 'address': ipaddr})
        form = IpForm(data=newdata)
        if form.is_valid():
            ip = form.save(commit=True)
            #cria log
            addlog(ip, "IP add", datetime.datetime.today(), user, "ip", ip.id)

            return redirect('ipdetail', ip.id)
        else:
            return render(request, 'forms/ip_edit.html', {'form': form, 'network': n, 'ipaddr': ipaddr, 'title':title})
    else:
        network = Network.objects.get(pk=pk)
        ipaddr = ipaddr
        form = IpFormnew()
        new = "ok"
        return render(request, 'forms/ip_edit.html', {'form': form, 'network': network, 'ipaddr': ipaddr, 'new': new, 'title':title})


@login_required(login_url='/ace/login/')
@permission_required('ace.change_ip', raise_exception=True)
def ip_edit(request, pk):
    user = request.user
    ip = get_object_or_404(Ip, pk=pk)
    if request.method == "POST":
        form = IpForm(request.POST, instance=ip)
        if form.is_valid():
            ip = form.save(commit=False)
            ip.save()
            #cria log
            addlog(ip, "IP edit", datetime.datetime.today(), user, "ip", ip.id)
            return redirect('ipdetail', ip.id)
        else:
            return render(request, 'forms/ip_edit.html', {'form': form})

    else:
        form = IpForm(instance=ip)
    return render(request, 'forms/ip_edit.html', {'form': form})


@login_required(login_url='/ace/login/')
@permission_required('ace.delete_ip', raise_exception=True)
def ip_delete(request, pk, template_name='ip_confirm_delete.html'):
    user = request.user
    ip = get_object_or_404(Ip, pk=pk)
    itens = Service.objects.filter(ip_id=pk)

    if itens:
        template = 'delete_error.html'
        tipo_item = "Serviço"
        return render(request, template, {'obj': ip, 'itens': itens, 'tipo_item': tipo_item})
    if request.method == 'POST':
        ip.delete()
        #cria log
        addlog(ip, "IP delete", datetime.datetime.today(), user, "ip", ip.id)
        return redirect('iplist')
    return render(request, template_name, {'ip': ip})


""" formularios Phone """


# Adiciona telefone já vinculando com o usuário
@login_required(login_url='/ace/login/')
@permission_required('ace.add_phone', raise_exception=True)
def phone_new(request):
    user = request.user
    phone_date = datetime.datetime.today()
    if request.method == "POST":
        form = PhoneForm(request.POST)

        if form.is_valid():
            userpk = form['user'].value()
            if userpk:
                phoneuser = User.objects.get(pk=userpk)
                phone = form.save(commit=True)
                phone.save()                
                p = Phoneownership(active=True, phone=phone, user=phoneuser)
                p.save()
                phone.active = True
                phone.save()

                #cria log
                if phone.password==False:
                    addlog(phone, "Phone add", phone_date, user, "phone", phone.id)
                else:
                    addlog(phone, "Password add", phone_date, user, "password", phone.id)

                #envia notificação de cadastro de telefone
                sendphone_notification(p.phone, p.user, phone_date, p)

                return redirect('phonedetail', phone.id)
            else:
                phone = form.save(commit=True)
                phone.save()                
                #cria log
                if phone.password==False:
                    addlog(phone, "Phone add", phone_date, user, "phone", phone.id)
                else:
                    addlog(phone, "Password add", phone_date, user, "password", phone.id)

                return redirect('phonedetail', phone.id)

        else:
            return render(request, 'forms/phone_edit.html', {'form': form})
    else:
        form = PhoneForm()
        return render(request, 'forms/phone_edit.html', {'form': form})


@login_required(login_url='/ace/login/')
@permission_required('ace.change_phone', raise_exception=True)
def phone_edit(request, pk):
    user = request.user    
    phone = get_object_or_404(Phone, pk=pk)
    phone_date = datetime.datetime.today()
    title = "Editar telefone"
    if request.method == "POST":
        form = PhoneForm(request.POST, instance=phone)
        if form.is_valid():
            userpk = form['user'].value()
            if userpk:
                phoneuser = User.objects.get(pk=userpk)
                phone = form.save(commit=False)
                phone.active = True
                phone.save()
                
                try:
                    po = Phoneownership.objects.get(phone=phone, active=True)   
                                
                    if po:
                        if po.user == phoneuser:
                            pass
                        else:
                            po.date_deactivation = phone_date
                            po.active = False
                            po.save()                        
                            p = Phoneownership(active=True, phone=phone, user=phoneuser)
                            p.save()
                            # envia notificação de cadastro de telefone
                            sendphone_notification(p.phone, p.user, phone_date, p)
                except:
                    p = Phoneownership(active=True, phone=phone, user=phoneuser)
                    p.save()
                    # envia notificação de cadastro de telefone
                    sendphone_notification(p.phone, p.user, phone_date, p)
                   
                
                #cria log
                if phone.password==False:
                    addlog(phone, "Phone edit", phone_date, user, "phone", phone.id)
                else:
                    addlog(phone, "Password edit", phone_date, user, "password", phone.id)

                return redirect('phonedetail', phone.id)
            else:
                phone = form.save(commit=False)

                try:
                    po = Phoneownership.objects.get(phone=phone, active=True)                  
                    if po:
                        po.date_deactivation = phone_date
                        po.active = False
                        po.save() 
                        phone.active = False 
                        phone.save()
                        # envia notificação de cadastro de telefone
                        sendphone_notification(p.phone, p.user, phone_date, po)

                except:
                        phone.active = False 
                        phone.save()                      

                #cria log
                if phone.password==False:
                    addlog(phone, "Phone edit", phone_date, user, "phone", phone.id)
                else:
                    addlog(phone, "Password edit", phone_date, user, "password", phone.id)

                return redirect('phonedetail', phone.id)
        else:
            return render(request, 'forms/phone_edit.html', {'form': form, 'title':title})


    else:
        form = PhoneForm(instance=phone)
    return render(request, 'forms/phone_edit.html', {'form': form, 'phone': phone, 'title':title})


@login_required(login_url='/ace/login/')
@permission_required('ace.delete_phone', raise_exception=True)
def phone_delete(request, pk, template_name='phone_confirm_delete.html'):
    user = request.user    
    phone = get_object_or_404(Phone, pk=pk)
    itens = Netpoint.objects.filter(phone_id=pk)
    phone_date = datetime.datetime.today()


    if itens:
        template = 'delete_error.html'
        return render(request, template, {'obj': phone, 'itens': itens})
    if request.method == 'POST':
        phone.delete()

        if phone.password == False:
            addlog(phone, "Phone delete", phone_date, user, "phone", phone.id)
        else:
            addlog(phone, "Password delete", phone_date, user, "password", phone.id)


        return redirect('phonelist')
    return render(request, template_name, {'phone': phone, })


""" formularios Place """


@login_required(login_url='/ace/login/')
@permission_required('ace.add_place', raise_exception=True)
def place_new(request):
    if request.method == "POST":
        form = PlaceForm(request.POST)

        if form.is_valid():
            place = form.save(commit=True)
            place.save()
            return redirect('placedetail', place.id)
        else:
            return render(request, 'forms/place_edit.html', {'form': form})
    else:
        form = PlaceForm()
        return render(request, 'forms/place_edit.html', {'form': form})


@login_required(login_url='/ace/login/')
@permission_required('ace.change_place', raise_exception=True)
def place_edit(request, pk):
    place = get_object_or_404(Place, pk=pk)
    if request.method == "POST":
        form = PlaceForm(request.POST, instance=place)
        if form.is_valid():
            place = form.save(commit=False)
            place.save()
            return redirect('placedetail', place.id)
        else:
            return render(request, 'forms/place_edit.html', {'form': form})

    else:
        form = PlaceForm(instance=place)
    return render(request, 'forms/place_edit.html', {'form': form})


@login_required(login_url='/ace/login/')
@permission_required('ace.delete_place', raise_exception=True)
def place_delete(request, pk, template_name='place_confirm_delete.html'):
    place = get_object_or_404(Place, pk=pk)
    racks = Rack.objects.filter(place_id=pk)
    phones = Phone.objects.filter(place_id=pk)
    netpoints = Netpoint.objects.filter(place_id=pk)
    switches = Switch.objects.filter(place_id=pk)
    itens = list(chain(racks, phones, netpoints, switches))

    if itens:
        template = 'delete_error.html'
        return render(request, template, {'obj': place, 'itens': itens})

    if request.method == 'POST':
        place.delete()
        return redirect('placelist')
    return render(request, template_name, {'place': place, })


@login_required(login_url='/ace/login/')
@permission_required('ace.add_sector', raise_exception=True)
def sector_new(request):
    if request.method == "POST":
        form = SectorFormModal(request.POST)

        if form.is_valid():
            sector = form.save(commit=True)
            sector.save()
            return redirect('sectordetail', sector.id)
        else:
            return render(request, 'forms/sector_edit.html', {'form': form})
    else:
        form = SectorFormModal()

        return render(request, 'forms/sector_edit.html', {'form': form})


@login_required(login_url='/ace/login/')
@permission_required('ace.change_sector', raise_exception=True)
def sector_edit(request, pk):
    sector = get_object_or_404(Sector, pk=pk)
    if request.method == "POST":
        form = SectorFormModal(request.POST, instance=sector)
        if form.is_valid():
            sector = form.save(commit=False)
            sector.save()
            return redirect('sectordetail', sector.id)
        else:
            return render(request, 'forms/sector_edit.html', {'form': form})

    else:
        form = SectorFormModal(instance=sector)
    return render(request, 'forms/sector_edit.html', {'form': form})


@login_required(login_url='/ace/login/')
@permission_required('ace.delete_sector', raise_exception=True)
def sector_delete(request, pk, template_name='sector_confirm_delete.html'):
    sector = get_object_or_404(Sector, pk=pk)
    place = Place.objects.filter(sector_id=pk)
    itens = place

    if itens:
        template = 'delete_error.html'
        return render(request, template, {'obj': sector, 'itens': itens})

    if request.method == 'POST':
        sector.delete()
        return redirect('sectorlist')
    return render(request, template_name, {'sector': sector, })


""" formularios Rack """


@login_required(login_url='/ace/login/')
@permission_required('ace.add_rack', raise_exception=True)
def rack_new(request):
    if request.method == "POST":
        form = RackForm(request.POST)
        if form.is_valid():
            rack = form.save(commit=True)
            rack.save()
            return redirect('rackdetail', rack.id)
        else:
            return render(request, 'forms/rack_edit.html', {'form': form})
    else:
        form = RackForm()
        return render(request, 'forms/rack_edit.html', {'form': form})


@login_required(login_url='/ace/login/')
@permission_required('ace.change_rack', raise_exception=True)
def rack_edit(request, pk):
    rack = get_object_or_404(Rack, pk=pk)
    if request.method == "POST":
        form = RackForm(request.POST, instance=rack)
        if form.is_valid():
            rack = form.save(commit=False)
            rack.save()
            return redirect('rackdetail', rack.id)
        else:
            return render(request, 'forms/rack_edit.html', {'form': form})

    else:
        form = RackForm(instance=rack)
    return render(request, 'forms/rack_edit.html', {'form': form})


@login_required(login_url='/ace/login/')
@permission_required('ace.delete_rack', raise_exception=True)
def rack_delete(request, pk, template_name='rack_confirm_delete.html'):
    rack = get_object_or_404(Rack, pk=pk)
    netpoints = Netpoint.objects.filter(rack_id=pk)
    switches = Switch.objects.filter(rack_id=pk)
    itens = list(chain(netpoints, switches))

    if itens:
        template = 'delete_error.html'
        return render(request, template, {'obj': rack, 'itens': itens})

    if request.method == 'POST':
        rack.delete()
        return redirect('racklist')
    return render(request, template_name, {'rack': rack, })


""" formularios Stack """


@login_required(login_url='/ace/login/')
@permission_required('ace.add_stack', raise_exception=True)
def stack_new(request):
    if request.method == "POST":
        form = StackForm(request.POST)
        if form.is_valid():
            stack = form.save(commit=True)
            stack.save()
            return redirect('stackdetail', stack.id)
        else:
            return render(request, 'forms/stack_edit.html', {'form': form})
    else:
        form = StackForm()
        return render(request, 'forms/stack_edit.html', {'form': form})


@login_required(login_url='/ace/login/')
@permission_required('ace.change_stack', raise_exception=True)
def stack_edit(request, pk):
    stack = get_object_or_404(Stack, pk=pk)
    if request.method == "POST":
        form = StackForm(request.POST, instance=stack)
        if form.is_valid():
            stack = form.save(commit=False)
            stack.save()
            return redirect('stackdetail', stack.id)
        else:
            return render(request, 'forms/stack_edit.html', {'form': form})
    else:
        form = StackForm(instance=stack)
    return render(request, 'forms/stack_edit.html', {'form': form})


@login_required(login_url='/ace/login/')
@permission_required('ace.delete_stack', raise_exception=True)
def stack_delete(request, pk, template_name='stack_confirm_delete.html'):
    stack = get_object_or_404(Stack, pk=pk)
    itens = Ip.objects.filter(device_id=pk)
    if itens:
        template = 'delete_error.html'
        tipo_item = "IP"
        return render(request, template, {'obj': stack, 'itens': itens, 'tipo_item': tipo_item})

    if request.method == 'POST':
        stack.delete()
        return redirect('stacklist')
    return render(request, template_name, {'stack': stack, })


""" formularios Switch """


@login_required(login_url='/ace/login/')
@permission_required('ace.add_switch', raise_exception=True)
def switch_new(request):
    user = request.user
    if request.method == "POST":
        form = SwitchForm(request.POST)

        if form.is_valid():
            switch = form.save(commit=True)
            switch.save()
            #cria log
            addlog(switch, "Switch add", datetime.datetime.today(), user, "switch", switch.id)
            return redirect('switchdetail', switch.id)
        else:
            return render(request, 'forms/switch_edit.html', {'form': form})
    else:
        form = SwitchForm()
        return render(request, 'forms/switch_edit.html', {'form': form, })


@login_required(login_url='/ace/login/')
@permission_required('ace.change_switch', raise_exception=True)
def switch_edit(request, pk):
    user = request.user    
    switch = get_object_or_404(Switch, pk=pk)
    if request.method == "POST":
        form = SwitchForm(request.POST, instance=switch)
        if form.is_valid():
            switch = form.save(commit=False)
            switch.save()
            #cria log
            addlog(switch, "Switch edit", datetime.datetime.today(), user, "switch", switch.id)
            return redirect('switchdetail', switch.id)
        else:
            return render(request, 'forms/switch_edit.html', {'form': form})

    else:
        form = SwitchForm(instance=switch)
    return render(request, 'forms/switch_edit.html', {'form': form})


@login_required(login_url='/ace/login/')
@permission_required('ace.delete_switch', raise_exception=True)
def switch_delete(request, pk, template_name='switch_confirm_delete.html'):
    user = request.user    
    switch = get_object_or_404(Switch, pk=pk)
    if request.method == 'POST':
        switch.delete()
        #cria log
        addlog(switch, "Switch delete", datetime.datetime.today(), user, "switch", switch.id)
        return redirect('switchlist')
    return render(request, template_name, {'switch': switch, })


""" formularios User """


@login_required(login_url='/ace/login/')
@permission_required('auth.add_user', raise_exception=True)
def user_new(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(user.password)
            user.save()
            return redirect('userdetail', user.id)
        else:
            return render(request, 'forms/user_edit.html', {'form': form})
    else:
        form = NewUserForm()
        return render(request, 'forms/user_edit.html', {'form': form})


@login_required(login_url='/ace/login/')
@permission_required('auth.change_user', raise_exception=True)
def user_edit(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == "POST":
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            return redirect('userdetail', user.id)
        else:
            return render(request, 'forms/user_edit.html', {'form': form})

    else:
        form = UserForm(instance=user)
    return render(request, 'forms/user_edit.html', {'form': form})


# def user_delete(request, pk, template_name='user_confirm_delete.html'):
#    user = get_object_or_404(User, pk=pk)
#    if request.method=='POST':
#        user.delete()
#        return redirect('userlist')
#    return render(request, template_name, {'user': user,})


@login_required(login_url='/ace/login/')
# @permission_required('auth.change_user',raise_exception=True)
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        title = "Mudança de senha"
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
        title = "Mudança de senha"
    return render(request, 'changepassword.html', {
        'form': form,
        'title': title,
    })


""" formularios Ownerid """


@login_required(login_url='/ace/login/')
@permission_required('ace.add_ownerid', raise_exception=True)
def ownerid_new(request):
    if request.method == "POST":
        form = OwneridForm(request.POST)
        if form.is_valid():
            ownerid = form.save(commit=True)
            ownerid.save()
            return redirect('owneriddetail', ownerid.id)
        else:
            return render(request, 'forms/ownerid_edit.html', {'form': form})
    else:
        form = OwneridForm()
        return render(request, 'forms/ownerid_edit.html', {'form': form})


@login_required(login_url='/ace/login/')
@permission_required('ace.change_ownerid', raise_exception=True)
def ownerid_edit(request, pk):
    ownerid = get_object_or_404(Ownerid, pk=pk)
    if request.method == "POST":
        form = OwneridForm(request.POST, instance=ownerid)
        if form.is_valid():
            ownerid = form.save(commit=False)
            ownerid.save()
            return redirect('owneriddetail', ownerid.id)
        else:
            return render(request, 'forms/ownerid_edit.html', {'form': form})

    else:
        form = OwneridForm(instance=ownerid)
    return render(request, 'forms/ownerid_edit.html', {'form': form})


""" formularios Netpoint """


@login_required(login_url='/ace/login/')
@permission_required('ace.add_netpoint', raise_exception=True)
def netpoint_new(request):
    if request.method == "POST":
        form = NetpointForm(request.POST)
        if form.is_valid():
            netpoint = form.save(commit=True)
            netpoint.save()
            return redirect('pointdetail', netpoint.id)
        else:
            return render(request, 'forms/point_edit.html', {'form': form})
    else:
        form = NetpointForm()
        return render(request, 'forms/point_edit.html', {'form': form})


@login_required(login_url='/ace/login/')
@permission_required('ace.change_netpoint', raise_exception=True)
def netpoint_edit(request, pk):
    netpoint = get_object_or_404(Netpoint, pk=pk)
    if request.method == "POST":
        form = NetpointForm(request.POST, instance=netpoint)
        if form.is_valid():
            netpoint = form.save(commit=False)
            netpoint.save()
            return redirect('pointdetail', netpoint.id)
        else:
            return render(request, 'forms/point_edit.html', {'form': form})

    else:
        form = NetpointForm(instance=netpoint)
    return render(request, 'forms/point_edit.html', {'form': form})


@login_required(login_url='/ace/login/')
@permission_required('ace.delte_netpoint', raise_exception=True)
def netpoint_delete(request, pk, template_name='point_confirm_delete.html'):
    netpoint = get_object_or_404(Netpoint, pk=pk)
    if request.method == 'POST':
        netpoint.delete()
        return redirect('netpointlist')
    return render(request, template_name, {'netpoint': netpoint, })


""" formularios Switchport """


@login_required(login_url='/ace/login/')
@permission_required('ace.add_switchport', raise_exception=True)
def switchport_new(request):
    if request.method == "POST":
        form = SwitchportForm(request.POST)
        if form.is_valid():
            switchport = form.save(commit=True)
            switchport.save()
            return redirect('swport', switchport.id)
        else:
            return render(request, 'forms/switchport_edit.html', {'form': form})
    else:
        form = SwitchportForm()
        return render(request, 'forms/switchport_edit.html', {'form': form})


@login_required(login_url='/ace/login/')
@permission_required('ace.change_switchport', raise_exception=True)
def switchport_edit(request, pk):
    switchport = get_object_or_404(Switchport, pk=pk)
    if request.method == "POST":
        form = SwitchportForm(request.POST, instance=switchport)
        if form.is_valid():
            # switchport = form.save(commit=False)
            switchport = form.save()
            switchport.save()
            return redirect('swport', switchport.id)
        else:
            return render(request, 'forms/switch_edit.html', {'form': form})

    else:
        form = SwitchportForm(instance=switchport)
    return render(request, 'forms/switchport_edit.html', {'form': form})


@login_required(login_url='/ace/login/')
@permission_required('ace.delete_switchport', raise_exception=True)
def switchport_delete(request, pk, template_name='switchport_confirm_delete.html'):
    switchport = get_object_or_404(Switchport, pk=pk)
    sw = switchport.switch
    if request.method == 'POST':
        switchport.delete()
        return redirect('switchdetail', sw.id)
    return render(request, template_name, {'switchport': switchport, })


""" formularios Patchpanel """


@login_required(login_url='/ace/login/')
@permission_required('ace.add_patchpanel', raise_exception=True)
def patchpanel_new(request):
    if request.method == "POST":
        form = PatchpanelForm(request.POST)
        if form.is_valid():
            patchpanel = form.save(commit=True)
            patchpanel.save()
            return redirect('patchpaneldetail', patchpanel.id)
        else:
            return render(request, 'forms/patchpanel_edit.html', {'form': form})
    else:
        form = PatchpanelForm()
        return render(request, 'forms/patchpanel_edit.html', {'form': form})


@login_required(login_url='/ace/login/')
@permission_required('ace.change_patchpanel', raise_exception=True)
def patchpanel_edit(request, pk):
    patchpanel = get_object_or_404(Patchpanel, pk=pk)
    if request.method == "POST":
        form = PatchpanelForm(request.POST, instance=patchpanel)
        if form.is_valid():
            patchpanel = form.save(commit=False)
            patchpanel.save()
            return redirect('patchpaneldetail', patchpanel.id)
        else:
            return render(request, 'forms/patchpanel_edit.html', {'form': form})
    else:
        form = PatchpanelForm(instance=patchpanel)
    return render(request, 'forms/patchpanel_edit.html', {'form': form})


@login_required(login_url='/ace/login/')
@permission_required('ace.delete_patchpanel', raise_exception=True)
def patchpanel_delete(request, pk, template_name='patchpanel_confirm_delete.html'):
    patchpanel = get_object_or_404(Patchpanel, pk=pk)
    if request.method == 'POST':
        patchpanel.delete()
        return redirect('patchpanellist')
    return render(request, template_name, {'patchpanel': patchpanel})


""" formularios Patchpanelport """


@login_required(login_url='/ace/login/')
@permission_required('ace.add_patchpanelport', raise_exception=True)
def patchpanelport_new(request):
    if request.method == "POST":
        form = PatchpanelportForm(request.POST)
        if form.is_valid():
            patchpanelport = form.save(commit=True)
            patchpanelport.save()
            return redirect('patchpanelport', patchpanelport.id)
        else:
            return render(request, 'forms/patchpanelport_edit.html', {'form': form})
    else:
        form = PatchpanelportForm()
        return render(request, 'forms/patchpanelport_edit.html', {'form': form})


@login_required(login_url='/ace/login/')
@permission_required('ace.change_patchpanelport', raise_exception=True)
def patchpanelport_edit(request, pk):
    patchpanelport = get_object_or_404(Patchpanelport, pk=pk)
    if request.method == "POST":
        form = PatchpanelportForm(request.POST, instance=patchpanelport)
        if form.is_valid():
            patchpanelport = form.save(commit=False)
            patchpanelport.save()
            return redirect('patchpanelport', patchpanelport.id)
        else:
            return render(request, 'forms/patchpanelport_edit.html', {'form': form})

    else:
        form = PatchpanelportForm(instance=patchpanelport)
    return render(request, 'forms/patchpanelport_edit.html', {'form': form})


@login_required(login_url='/ace/login/')
@permission_required('ace.delete_patchpanelport', raise_exception=True)
def patchpanelport_delete(request, pk, template_name='patchpanelport_confirm_delete.html'):
    patchpanelport = get_object_or_404(Patchpanelport, pk=pk)
    if request.method == 'POST':
        patchpanelport.delete()
        return redirect('patchpanellist')
    return render(request, template_name, {'patchpanelport': patchpanelport})


""" formularios Posse telefone """


@login_required(login_url='/ace/login/')
@permission_required('ace.add_phoneownership', raise_exception=True)
def phoneownership_new(request, pk):
    user = request.user
    phone = get_object_or_404(Phone, pk=pk)
    po = Phoneownership.objects.filter(phone=phone, active=True)
    today = datetime.datetime.now()
    if not po:

        if request.method == "POST":
            form = PhoneownershipForm(request.POST)
            p = form['place'].value()
            t = form['telephonetype'].value()
            c = form['phonecategory'].value()

            if c:
                phonecategory = Phonecategory.objects.get(pk=c)

            if p:
                place = get_object_or_404(Place, pk=p)
                phone.place = place

            if t:
                phonetype = get_object_or_404(Phonetype, pk=t)
                phone.telephonetype = phonetype

            if form.is_valid():
                phoneownership = form.save(commit=False)
                phoneownership.phone = phone
                phoneownership.save()
                p = phoneownership
                phone.active = True
                phone.user = phoneownership.user
                phone.phonecategory = phonecategory
                phone.save()

                # envia notificação de cadastro de telefone
                sendphone_notification(p.phone, p.user, today, p)

                if p.phone.password == True:
                    addlog(p.phone.user, "password association", datetime.datetime.today(), user, 'password', phone.id)
                else:
                    addlog(p.phone, "phone association", datetime.datetime.today(), user, 'phone', phone.id)

                return redirect('phonedetail', phone.id)
            else:
                return render(request, 'forms/phoneownership_edit.html', {'form': form, 'phone': phone})

        else:
            form = PhoneownershipForm()
            phone = get_object_or_404(Phone, pk=pk)
            # return render(request, 'phoneownership_edit.html', {'form': form})
            return render(request, 'forms/phoneownership_edit.html', {'form': form, 'phone': phone})
    else:
        return redirect('phonedetail', phone.id)

@permission_required('ace.delete_phoneownership', raise_exception=True)
def phoneownership_disable(request, pk):
    user = request.user
    today = datetime.datetime.now()
    phone = get_object_or_404(Phone, pk=pk)
    phoneownership = Phoneownership.objects.get(phone=phone, active=True)
    if phone.active == True or phoneownership:

        if phoneownership:
            phoneownership.date_deactivation = today
            phoneownership.active = False
            phoneownership.save()
            p = phoneownership
            phone.active = False
            phone.phonecategory = None
            phone.telephonetype = None
            phone.user = None
            phone.place = None
            phone.save()
            # envia notificação de cadastro de telefone
            sendphone_notification(p.phone, p.user, today, p)

            if p.phone.password == True:
                addlog(p.user, "password disassociation", datetime.datetime.today(), user, 'password', phone.id)
            else:
                addlog(p.phone, "phone disassociation", datetime.datetime.today(), user, 'phone', phone.id)

            return redirect('phonedetail', phone.id)

    else:

        return redirect('phonedetail', phone.id)





""" formularios VLAN """


@login_required(login_url='/ace/login/')
@permission_required('ace.add_vlan', raise_exception=True)
def vlan_new(request):
    title = "Editar VLAN"    
    if request.method == "POST":
        form = VlanForm(request.POST)
        if form.is_valid():
            vlan = form.save(commit=True)
            vlan.save()
            return redirect('vlandetail', vlan.id)
        else:
            return render(request, 'forms/vlan_edit.html', {'form': form, 'title':title,})
    else:
        form = VlanForm()
        return render(request, 'forms/vlan_edit.html', {'form': form, 'title':title,})


@login_required(login_url='/ace/login/')
@permission_required('ace.change_vlan', raise_exception=True)
def vlan_edit(request, pk):
    title = "Editar VLAN"
    vlan = get_object_or_404(Vlan, pk=pk)
    if request.method == "POST":
        form = VlanForm(request.POST, instance=vlan)
        if form.is_valid():
            vlan = form.save(commit=False)
            vlan.save()
            return redirect('vlandetail', vlan.id)
        else:
            return render(request, 'forms/vlan_edit.html', {'form': form, 'vlan': vlan, 'title':title, })

    else:
        form = VlanForm(instance=vlan)
    return render(request, 'forms/vlan_edit.html', {'form': form, 'vlan': vlan, 'title':title, })


@login_required(login_url='/ace/login/')
@permission_required('ace.delete_vlan', raise_exception=True)
def vlan_delete(request, pk, template_name='vlan_confirm_delete.html'):
    vlan = get_object_or_404(Vlan, pk=pk)
    try:
        networks = Network.objects.filter(vln_id=pk)
        switchports = Switchport.objects.filter(vln_id=pk)
            
        if networks or switchports:
            itens = list(chain(networks, switchports))
            # if networks:
            template = 'delete_error.html'
            return render(request, template, {'obj': vlan, 'itens': itens})
    except:

        if request.method == 'POST':
            vlan.delete()
            return redirect('vlanlist')
        return render(request, template_name, {'vlan': vlan})


""" formularios Update """


@login_required(login_url='/ace/login/')
@permission_required('ace.add_hostupdate', raise_exception=True)
def update_new(request, pk):
    host = Host.objects.get(pk=pk)
    if request.method == "POST":
        form = UpdateForm(request.POST)
        if form.is_valid():
            update = form.save(commit=False)
            update.host = host
            update.save()
            return redirect('hostdetail', update.host.id)
        else:
            return render(request, 'forms/update_edit.html', {'form': form, 'host': host})
    else:
        form = UpdateForm()
        return render(request, 'forms/update_edit.html', {'form': form, 'host': host})


@login_required(login_url='/ace/login/')
@permission_required('ace.change_update', raise_exception=True)
def update_edit(request, pk, h):
    host = Host.objects.get(pk=h)
    update = get_object_or_404(Hostupdate, pk=pk)
    if request.method == "POST":
        form = UpdateForm(request.POST, instance=update)
        if form.is_valid():
            update = form.save(commit=False)
            update.host = host
            update.save()
            return redirect('hostdetail', update.host.id)
        else:
            return render(request, 'forms/update_edit.html', {'form': form, 'host': host})

    else:
        form = UpdateForm(instance=update)
    return render(request, 'forms/update_edit.html', {'form': form, 'host': host})


""" envio de senha por email """


@login_required(login_url='/ace/login/')
def send_password(request, pk):
    # password = Phonepassword.objects.get(pk=pk)
    phone = Phone.objects.get(pk=pk)
    # c = password.code
    c = phone.num
    # u = password.user
    u = phone.user
    # email = password.user.email
    email = phone.user.email
    # t = password.passwordtype
    t = phone.phonecategory
    # config = AceConfig.objects.get()

    try:
        config = AceConfig.objects.get()
        from_email = config.email_from
        co_email = config.email_co

    except AceConfig.DoesNotExist:
        return render(request, 'phonedetail.html', {'ramal': phone, })

    # from_email = config.email_from
    # co_email = config.email_co

    if email == '':
        return render(request, 'phonedetail.html', {'ramal': phone, })

    else:
        send = 'ok'
        message = EmailMessage('email/email.tpl', {'c': c, 'u': u, 't': t, }, from_email, to=[email], bcc=[co_email])
        message.send()
        # return render(request, 'password.html', {'senha': password, 'send': send})
        return render(request, 'phonedetail.html', {'ramal': phone, 'send': send})


""" janelas modal (ligthbox) """


#@permission_required('ace.add_place',raise_exception=True)
class PlaceCreateModal(ModalCreateView):

    def __init__(self, *args, **kwargs):
        super(PlaceCreateModal, self).__init__(*args, **kwargs)
        self.title = "Adicionar Local"
        self.submit_button.value = "Salvar"
        self.close_button.value = "Fechar"

        self.form_class = PlaceForm

    def form_valid(self, form, **kwargs):
        """
            The form_valid have to return the parent form_valid.
            In this example I will show you the two most populare case.
            The first you want just display a success message without the new object
        """
        self.response = ModalResponse("Local adicionado", "success")
        return super(PlaceCreateModal, self).form_valid(form, **kwargs)

        """
            The second, you want use the new object
        """
        # self.save(form) #When you save the form an attribute name object is created.
        # self.response = ModalResponse("{obj} is created".format(obj=self.object), 'success')
        # When you call the parent method you set commit to false because you have save the object.
        # return super(MyCreateModaln self).form_valid(form, commit=False, **kwargs)


# @permission_required('ace.add_ip',raise_exception=True)
class IpCreateModal(ModalCreateView):

    def __init__(self, *args, **kwargs):
        super(IpCreateModal, self).__init__(*args, **kwargs)
        self.title = "Adicionar IP"
        self.submit_button.value = "Salvar"
        self.close_button.value = "Fechar"

        self.form_class = IpFormModal

    def form_valid(self, form, **kwargs):
        """
            The form_valid have to return the parent form_valid.
            In this example I will show you the two most populare case.
            The first you want just display a success message without the new object
        """
        self.response = ModalResponse("Ip adicionado", "success")
        return super(IpCreateModal, self).form_valid(form, **kwargs)


class HostCreateModal(ModalCreateView):

    def __init__(self, *args, **kwargs):
        super(HostCreateModal, self).__init__(*args, **kwargs)
        self.title = "Adicionar Equipamento/Servidor"
        self.submit_button.value = "Salvar"
        self.close_button.value = "Fechar"

        self.form_class = HostForm

    def form_valid(self, form, **kwargs):
        """
            The form_valid have to return the parent form_valid.
            In this example I will show you the two most populare case.
            The first you want just display a success message without the new object
        """
        self.response = ModalResponse("Equipamento/Servidor adicionado", "success")
        return super(HostCreateModal, self).form_valid(form, **kwargs)



class ServiceCreateModal(ModalCreateView):

    def __init__(self, *args, **kwargs):
        super(ServiceCreateModal, self).__init__(*args, **kwargs)
        self.title = "Adicionar Serviço"
        self.submit_button.value = "Salvar"
        self.close_button.value = "Fechar"

        self.form_class = ServiceFormModal

    def form_valid(self, form, **kwargs):
        """
            The form_valid have to return the parent form_valid.
            In this example I will show you the two most populare case.
            The first you want just display a success message without the new object
        """
        self.response = ModalResponse("Serviço adicionado", "success")
        return super(ServiceCreateModal, self).form_valid(form, **kwargs)


class ServiceCategoryCreateModal(ModalCreateView):

    def __init__(self, *args, **kwargs):
        super(ServiceCategoryCreateModal, self).__init__(*args, **kwargs)
        self.title = "Adicionar Categoria de Serviço"
        self.submit_button.value = "Salvar"
        self.close_button.value = "Fechar"

        self.form_class = ServiceCategoryFormModal

    def form_valid(self, form, **kwargs):
        """
            The form_valid have to return the parent form_valid.
            In this example I will show you the two most populare case.
            The first you want just display a success message without the new object
        """
        self.response = ModalResponse("Categoria de Serviço adicionada", "success")
        return super(ServiceCategoryCreateModal, self).form_valid(form, **kwargs)


class FloorCreateModal(ModalCreateView):

    def __init__(self, *args, **kwargs):
        super(FloorCreateModal, self).__init__(*args, **kwargs)
        self.title = "Adicionar Andar"
        self.submit_button.value = "Salvar"
        self.close_button.value = "Fechar"

        self.form_class = FloorFormModal

    def form_valid(self, form, **kwargs):
        """
            The form_valid have to return the parent form_valid.
            In this example I will show you the two most populare case.
            The first you want just display a success message without the new object
        """
        self.response = ModalResponse("Andar adicionado", "success")
        return super(FloorCreateModal, self).form_valid(form, **kwargs)


class UserCreateModal(ModalCreateView):

    def __init__(self, *args, **kwargs):
        super(UserCreateModal, self).__init__(*args, **kwargs)
        self.title = "Adicionar Usuário"
        self.submit_button.value = "Salvar"
        self.close_button.value = "Fechar"

        self.form_class = UserFormModal
        # self.form_class = NewUserForm

    def form_valid(self, form, **kwargs):
        """
            The form_valid have to return the parent form_valid.
            In this example I will show you the two most populare case.
            The first you want just display a success message without the new object
        """
        self.response = ModalResponse("Usuário adicionado", "success")
        return super(UserCreateModal, self).form_valid(form, **kwargs)


class OwneridCreateModal(ModalCreateView):

    def __init__(self, *args, **kwargs):
        super(OwneridCreateModal, self).__init__(*args, **kwargs)
        self.title = "Adicionar Patrimônio"
        self.submit_button.value = "Salvar"
        self.close_button.value = "Fechar"

        self.form_class = OwneridForm

    def form_valid(self, form, **kwargs):
        """
            The form_valid have to return the parent form_valid.
            In this example I will show you the two most populare case.
            The first you want just display a success message without the new object
        """
        self.response = ModalResponse("Patrimônio adicionado", "success")
        return super(OwneridCreateModal, self).form_valid(form, **kwargs)


class ManufactorerCreateModal(ModalCreateView):

    def __init__(self, *args, **kwargs):
        super(ManufactorerCreateModal, self).__init__(*args, **kwargs)
        self.title = "Adicionar Fabricante"
        self.submit_button.value = "Salvar"
        self.close_button.value = "Fechar"

        self.form_class = ManufactorerForm

    def form_valid(self, form, **kwargs):
        """
            The form_valid have to return the parent form_valid.
            In this example I will show you the two most populare case.
            The first you want just display a success message without the new object
        """
        self.response = ModalResponse("Fabricante adicionado", "success")
        return super(ManufactorerCreateModal, self).form_valid(form, **kwargs)


class RackCreateModal(ModalCreateView):

    def __init__(self, *args, **kwargs):
        super(RackCreateModal, self).__init__(*args, **kwargs)
        self.title = "Adicionar Rack"
        self.submit_button.value = "Salvar"
        self.close_button.value = "Fechar"

        self.form_class = RackFormModal

    def form_valid(self, form, **kwargs):
        """
            The form_valid have to return the parent form_valid.
            In this example I will show you the two most populare case.
            The first you want just display a success message without the new object
        """
        self.response = ModalResponse("Rack adicionado", "success")
        return super(RackCreateModal, self).form_valid(form, **kwargs)


class StackCreateModal(ModalCreateView):

    def __init__(self, *args, **kwargs):
        super(StackCreateModal, self).__init__(*args, **kwargs)
        self.title = "Adicionar Pilha"
        self.submit_button.value = "Salvar"
        self.close_button.value = "Fechar"

        self.form_class = StackFormModal

    def form_valid(self, form, **kwargs):
        """
            The form_valid have to return the parent form_valid.
            In this example I will show you the two most populare case.
            The first you want just display a success message without the new object
        """
        self.response = ModalResponse("Pilha adicionada", "success")
        return super(StackCreateModal, self).form_valid(form, **kwargs)


class SwitchCreateModal(ModalCreateView):

    def __init__(self, *args, **kwargs):
        super(SwitchCreateModal, self).__init__(*args, **kwargs)
        self.title = "Adicionar Switch"
        self.submit_button.value = "Salvar"
        self.close_button.value = "Fechar"

        self.form_class = SwitchFormModal

    def form_valid(self, form, **kwargs):
        """
            The form_valid have to return the parent form_valid.
            In this example I will show you the two most populare case.
            The first you want just display a success message without the new object
        """
        self.response = ModalResponse("Switch adicionado", "success")
        return super(SwitchCreateModal, self).form_valid(form, **kwargs)


class NetworkCreateModal(ModalCreateView):

    def __init__(self, *args, **kwargs):
        super(NetworkCreateModal, self).__init__(*args, **kwargs)
        self.title = "Adicionar Rede"
        self.submit_button.value = "Salvar"
        self.close_button.value = "Fechar"

        self.form_class = NetworkForm

    def form_valid(self, form, **kwargs):
        """
            The form_valid have to return the parent form_valid.
            In this example I will show you the two most populare case.
            The first you want just display a success message without the new object
        """
        self.response = ModalResponse("Rede adicionada", "success")
        return super(NetworkCreateModal, self).form_valid(form, **kwargs)


class PatchpanelCreateModal(ModalCreateView):

    def __init__(self, *args, **kwargs):
        super(PatchpanelCreateModal, self).__init__(*args, **kwargs)
        self.title = "Adicionar Patchpanel"
        self.submit_button.value = "Salvar"
        self.close_button.value = "Fechar"

        self.form_class = PatchpanelForm

    def form_valid(self, form, **kwargs):
        """
            The form_valid have to return the parent form_valid.
            In this example I will show you the two most populare case.
            The first you want just display a success message without the new object
        """
        self.response = ModalResponse("Patchpanel adicionado", "success")
        return super(PatchpanelCreateModal, self).form_valid(form, **kwargs)


class PatchpanelportCreateModal(ModalCreateView):

    def __init__(self, *args, **kwargs):
        super(PatchpanelportCreateModal, self).__init__(*args, **kwargs)
        self.title = "Adicionar porta de Patchpanel"
        self.submit_button.value = "Salvar"
        self.close_button.value = "Fechar"

        self.form_class = PatchpanelportForm

    def form_valid(self, form, **kwargs):
        """
            The form_valid have to return the parent form_valid.
            In this example I will show you the two most populare case.
            The first you want just display a success message without the new object
        """
        self.response = ModalResponse("Porta de patchpanel adicionada", "success")
        return super(PatchpanelportCreateModal, self).form_valid(form, **kwargs)


class OsCreateModal(ModalCreateView):

    def __init__(self, *args, **kwargs):
        super(OsCreateModal, self).__init__(*args, **kwargs)
        self.title = "Adicionar sistema operacional"
        self.submit_button.value = "Salvar"
        self.close_button.value = "Fechar"

        self.form_class = OsFormModal

    def form_valid(self, form, **kwargs):
        """
            The form_valid have to return the parent form_valid.
            In this example I will show you the two most populare case.
            The first you want just display a success message without the new object
        """
        self.response = ModalResponse("Sistema operacional adicionado", "success")
        return super(OsCreateModal, self).form_valid(form, **kwargs)


class HosttypeCreateModal(ModalCreateView):

    def __init__(self, *args, **kwargs):
        super(HosttypeCreateModal, self).__init__(*args, **kwargs)
        self.title = "Adicionar tipo de equipamento"
        self.submit_button.value = "Salvar"
        self.close_button.value = "Fechar"

        self.form_class = HosttypeFormModal

    def form_valid(self, form, **kwargs):
        """
            The form_valid have to return the parent form_valid.
            In this example I will show you the two most populare case.
            The first you want just display a success message without the new object
        """
        self.response = ModalResponse("Tipo de equipamento adicionado", "success")
        return super(HosttypeCreateModal, self).form_valid(form, **kwargs)


class PhonecategoryCreateModal(ModalCreateView):

    def __init__(self, *args, **kwargs):
        super(PhonecategoryCreateModal, self).__init__(*args, **kwargs)
        self.title = "Adicionar categoria de telefone"
        self.submit_button.value = "Salvar"
        self.close_button.value = "Fechar"

        self.form_class = PhonecategoryFormModal

    def form_valid(self, form, **kwargs):
        """
            The form_valid have to return the parent form_valid.
            In this example I will show you the two most populare case.
            The first you want just display a success message without the new object
        """
        self.response = ModalResponse("Categoria de telefone adicionada", "success")
        return super(PhonecategoryCreateModal, self).form_valid(form, **kwargs)


class SwitchportCreateModal(ModalCreateView):

    def __init__(self, *args, **kwargs):
        super(SwitchportCreateModal, self).__init__(*args, **kwargs)
        self.title = "Adicionar porta de switch"
        self.submit_button.value = "Salvar"
        self.close_button.value = "Fechar"

        self.form_class = SwitchportFormModal

    def form_valid(self, form, **kwargs):
        """
            The form_valid have to return the parent form_valid.
            In this example I will show you the two most populare case.
            The first you want just display a success message without the new object
        """
        self.response = ModalResponse("Porta de switch adicionada", "success")
        return super(SwitchportCreateModal, self).form_valid(form, **kwargs)


class SectorCreateModal(ModalCreateView):

    def __init__(self, *args, **kwargs):
        super(SectorCreateModal, self).__init__(*args, **kwargs)
        self.title = "Adicionar setor/departamento"
        self.submit_button.value = "Salvar"
        self.close_button.value = "Fechar"

        self.form_class = SectorFormModal

    def form_valid(self, form, **kwargs):
        """
            The form_valid have to return the parent form_valid.
            In this example I will show you the two most populare case.
            The first you want just display a success message without the new object
        """
        self.response = ModalResponse("Setor/Departamento adicionado", "success")
        return super(SectorCreateModal, self).form_valid(form, **kwargs)


class DevicemodelCreateModal(ModalCreateView):

    def __init__(self, *args, **kwargs):
        super(DevicemodelCreateModal, self).__init__(*args, **kwargs)
        self.title = "Adicionar modelo de equipamento"
        self.submit_button.value = "Salvar"
        self.close_button.value = "Fechar"

        self.form_class = DevicemodelForm

    def form_valid(self, form, **kwargs):
        self.response = ModalResponse("Modelo de equipamento adicionado", "success")
        return super(DevicemodelCreateModal, self).form_valid(form, **kwargs)


class PhoneCreateModal(ModalCreateView):

    def __init__(self, *args, **kwargs):
        super(PhoneCreateModal, self).__init__(*args, **kwargs)
        self.title = "Adicionar telefone"
        self.submit_button.value = "Salvar"
        self.close_button.value = "Fechar"

        self.form_class = PhoneForm

    def form_valid(self, form, **kwargs):
        self.response = ModalResponse("Telefone adicionado", "success")
        return super(PhoneCreateModal, self).form_valid(form, **kwargs)


class PhonetypeCreateModal(ModalCreateView):

    def __init__(self, *args, **kwargs):
        super(PhonetypeCreateModal, self).__init__(*args, **kwargs)
        self.title = "Adicionar tipo/tecnologia de telefone"
        self.submit_button.value = "Salvar"
        self.close_button.value = "Fechar"

        self.form_class = PhonetypeForm

    def form_valid(self, form, **kwargs):
        self.response = ModalResponse("Tipo de telefone adicionado", "success")
        return super(PhonetypeCreateModal, self).form_valid(form, **kwargs)


class VlanCreateModal(ModalCreateView):

    def __init__(self, *args, **kwargs):
        super(VlanCreateModal, self).__init__(*args, **kwargs)
        self.title = "Adicionar VLAN"
        self.submit_button.value = "Salvar"
        self.close_button.value = "Fechar"

        self.form_class = VlanForm

    def form_valid(self, form, **kwargs):
        self.response = ModalResponse("Vlan adicionada", "success")
        return super(VlanCreateModal, self).form_valid(form, **kwargs)
