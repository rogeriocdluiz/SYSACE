# -*- coding: utf-8 -*-

#from ace.models import Switch, Netpoint, Phone, Switchport, Place, Stack, Rack, Host, Service, Ip, Network, Ownerid, Device, Servicecategory, User, AceConfig
from ace.models import *

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse

from django.contrib.auth.decorators import login_required, permission_required


import cStringIO as StringIO
import ho.pisa as pisa
from django.template.loader import get_template
from django.template import Context
from cgi import escape
from PIL import Image

from ace.models import AceConfig
#config = AceConfig.objects.get()




#org = config.org


def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = StringIO.StringIO()

    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("utf-8")), result, link_callback=fetch_resources)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return HttpResponse('We had some errors<pre>%s</pre>' % escape(html))

def fetch_resources(uri, rel):
    #path = os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ""))
    path = os.path.join(uri.replace(settings.STATIC_URL, ""))
    return path    







@login_required(login_url='/login/')
def placereport(request, local_id):
    try:
        config = AceConfig.objects.get()
        org = config.org

    except AceConfig.DoesNotExist:
        config = ""    
        org = ""

    local = Place.objects.get(pk=local_id)
    result = Netpoint.objects.all().filter(place=local)
    total = result.count()
    phoneresult = Phone.objects.all().filter(place=local)
    phonetotal = phoneresult.count()	
    title = "Relat&oacute;rio de pontos e telefones"
    return render_to_pdf(
            'reports/placereport.html',
            {
                'pagesize':'landscape',
                'mylist': result,
                'phonelist': phoneresult,
                'local': local,
                'total': total,
                'phonetotal': phonetotal,
                'org':org,
                'title':title,
            }
        )

@login_required(login_url='/login/')
def placereportblank(request):

    try:
        config = AceConfig.objects.get()
        org = config.org

    except AceConfig.DoesNotExist:
        config = ""    
        org = ""
    
    title = "Relat&oacute;rio de pontos de rede/telefones"
    return render_to_pdf(
            'reports/placereportblank.html',
            {
                'pagesize':'landscape',
                'title':title,
                'org':org,
                
            }
        )


@login_required(login_url='/login/')
def freepointsreport(request):

    try:
        config = AceConfig.objects.get()
        org = config.org

    except AceConfig.DoesNotExist:
        config = ""    
        org = ""

    p = Netpoint.objects.filter(pointtype='desativado').order_by('place__name')
    total = p.count()
    title = "Relat&oacute;rio de pontos de rede livres"
    return render_to_pdf(
            'reports/freepointsreport.html',
            {
                'pagesize':'A4',
                'mylist': p,
                'total': total,
                'org':org,
                'title':title,
            }
        )


@login_required(login_url='/login/')
def netpointsreport(request):

    try:
        config = AceConfig.objects.get()
        org = config.org

    except AceConfig.DoesNotExist:
        config = ""    
        org = ""

    p = Netpoint.objects.all().order_by('place__name')
    #p = Netpoint.objects.all()
    total = p.count()
    title = "Relat&oacute;rio de pontos"
    return render_to_pdf(
            'reports/netpointsreport.html',
            {
                'pagesize':'A4',
                'mylist': p,
                'total': total,
                'org':org,
                'title':title,
            }
        )



@login_required(login_url='/login/')
def switchreport(request):

    try:
        config = AceConfig.objects.get()
        org = config.org

    except AceConfig.DoesNotExist:
        config = ""    
        org = ""

    s = Switch.objects.all()
    total = s.count()
    title = "Relat&oacute;rio de switches"
    return render_to_pdf(
            'reports/switchreport.html',
            {
                'pagesize':'A4',
                'mylist': s,
                'total': total,
                'org':org,
                'title':title,
            }
        )

@login_required(login_url='/login/')
def hostreport(request):

    try:
        config = AceConfig.objects.get()
        org = config.org

    except AceConfig.DoesNotExist:
        config = ""    
        org = ""

    h = Host.objects.all()
    total = h.count()
    title = "Relat&oacute;rio de equipamentos"
    return render_to_pdf(
            'reports/hostreport.html',
            {
                'pagesize':'landscape',
                'mylist': h,
                'total': total,
                'org':org,
                'title':title,
            }
        )


@login_required(login_url='/login/')
def printerreport(request):

    try:
        config = AceConfig.objects.get()
        org = config.org

    except AceConfig.DoesNotExist:
        config = ""    
        org = ""    
    p = Printer.objects.all()
    total = p.count()
    title = "Relat&oacute;rio de impressoras"
    return render_to_pdf(
            'reports/printerreport.html',
            {
                'pagesize':'landscape',
                'mylist': p,
                'total': total,
                'org':org,
                'title':title,
            }
        )



@login_required(login_url='/login/')
def hostdetailreport(request, host_id):

    try:
        config = AceConfig.objects.get()
        org = config.org

    except AceConfig.DoesNotExist:
        config = ""    
        org = ""

    host = Host.objects.get(pk=host_id)
    swport = Switchport.objects.filter(host=host_id)
    i = Ip.objects.filter(device=host_id)
    s = []
    for ip in i:
        try:
            service = Service.objects.get(ip=ip)
            if service:
                s.append(service)
            stotal = s.count()
        except:
            stotal = 0


    u = host.hostupdate_set.all()    
    swporttotal = swport.count()
    itotal = i.count()
    utotal = u.count()
    title = "Relat&oacute;rio do equipamento"
    return render_to_pdf(
            'reports/hostdetailreport.html',
            {
                'pagesize':'A4',
                'host':host,
                'swport': swport,
                'i': i,
                's': s,
                'swporttotal': swporttotal,
                'itotal': itotal,
                'stotal': stotal,
                'org':org,
                'title':title,
                's':s,
                'u':u,
                'utotal':utotal,
            }
        )






@login_required(login_url='/login/')
def ipreport(request):

    try:
        config = AceConfig.objects.get()
        org = config.org

    except AceConfig.DoesNotExist:
        config = ""    
        org = ""

    i = Ip.objects.all()
    total = i.count()
    title = "Relat&oacute;rio de IPs"
    return render_to_pdf(
            'reports/ipreport.html',
            {
                'pagesize':'A4',
                'mylist': i,
                'total': total,
                'org':org,
                'title':title
            }
        )


@login_required(login_url='/login/')
def servicereport(request):

    try:
        config = AceConfig.objects.get()
        org = config.org

    except AceConfig.DoesNotExist:
        config = ""    
        org = ""

    s = Service.objects.all()
    total = s.count()
    title = u"Relat&oacute;rio de servi&ccedil;os"
    return render_to_pdf(
            'reports/servicereport.html',
            {
                'pagesize':'A4',
                'mylist': s,
                'total': total,
                'org':org,
                'title':title
            }
        )	





@login_required(login_url='/login/')
@permission_required('ace.view_password',raise_exception=True)
def pwreport(request):

    try:
        config = AceConfig.objects.get()
        org = config.org

    except AceConfig.DoesNotExist:
        config = ""    
        org = ""    
    p = Phone.objects.filter(password=True, active=True)
    total = p.count()
    title = u"Relat&oacute;rio de senhas"
    return render_to_pdf(
            'reports/pwreport.html',
            {
                'pagesize':'A4',
                'mylist': p,
                'total': total,
                'org':org,
                'title':title
            }
        )    


@login_required(login_url='/login/')
def pwreportopen(request):

    try:
        config = AceConfig.objects.get()
        org = config.org

    except AceConfig.DoesNotExist:
        config = ""    
        org = ""   
    report = "open"     
    p = Phone.objects.filter(password=True, active=True)
    total = p.count()
    title = u"Relat&oacute;rio de senhas"
    return render_to_pdf(
            'reports/pwreport.html',
            {
                'pagesize':'A4',
                'mylist': p,
                'total': total,
                'org':org,
                'title':title,
                'report':report
            }
        )    





@login_required(login_url='/login/')
#@permission_required('ace.view_phone',raise_exception=True)
def phonereport(request):

    try:
        config = AceConfig.objects.get()
        org = config.org

    except AceConfig.DoesNotExist:
        config = ""    
        org = ""

    p = Phone.objects.filter(password=False, active=True).order_by('place')
    total = p.count()
    title = u"Relat&oacute;rio de telefones"
    return render_to_pdf(
            'reports/phonereport.html',
            {
                'pagesize':'A4',
                'mylist': p,
                'total': total,
                'org':org,
                'title':title
            }
        ) 



@login_required(login_url='/login/')
def rackreport(request, rack_id):

    try:
        config = AceConfig.objects.get()
        org = config.org

    except AceConfig.DoesNotExist:
        config = ""    
        org = ""

    rack = Rack.objects.get(pk=rack_id)
    p = Netpoint.objects.filter(rack=rack)
    total = p.count()
    title ="Relat&oacute;rio de rack"
    return render_to_pdf(
            'reports/rackreport.html',
            {
                'pagesize':'A4',
                'mylist': p,
                'total': total,
                'title':title,
                'rack':rack,
                'org':org,
            }
        )      

