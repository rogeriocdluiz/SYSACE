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


#config = AceConfig.objects.get()
try:
    config = AceConfig.objects.get()
    org = config.org

except AceConfig.DoesNotExist:
    config = ""    
    org = ""



#org = config.org


def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    context = Context(context_dict)
    html  = template.render(context)
    result = StringIO.StringIO()

    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("utf-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return HttpResponse('We had some errors<pre>%s</pre>' % escape(html))



@login_required(login_url='/login/')
def placereport(request, local_id):
    local = Place.objects.get(pk=local_id)
    result = Netpoint.objects.all().filter(place=local)
    total = result.count()
    phoneresult = Phone.objects.all().filter(place=local)
    phonetotal = phoneresult.count()	
    title = "Relatório de pontos e telefones"
    return render_to_pdf(
            'ace/reports/placereport.html',
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
    
    title = "Relatório de pontos de rede/telefones"
    return render_to_pdf(
            'ace/reports/placereportblank.html',
            {
                'pagesize':'landscape',
                'title':title,
                'org':org,
                
            }
        )


@login_required(login_url='/login/')
def freepointsreport(request):
    p = Netpoint.objects.filter(pointtype='desativado')
    total = p.count()
    title = "Relatório de pontos de rede livres"
    return render_to_pdf(
            'ace/reports/freepointsreport.html',
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
    p = Netpoint.objects.all().order_by('place__name')
    total = p.count()
    title = "Relatório de pontos"
    return render_to_pdf(
            'ace/reports/netpointsreport.html',
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
    s = Switch.objects.all()
    total = s.count()
    title = "Relatório de switches"
    return render_to_pdf(
            'ace/reports/switchreport.html',
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
    h = Host.objects.all()
    total = h.count()
    title = "Relatório de equipamentos"
    return render_to_pdf(
            'ace/reports/hostreport.html',
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
    p = Printer.objects.all()
    total = p.count()
    title = "Relatório de equipamentos"
    return render_to_pdf(
            'ace/reports/printerreport.html',
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
    host = Host.objects.get(pk=host_id)
    swport = Switchport.objects.all().filter(host=host_id)
    i = Ip.objects.all().filter(device=host_id)
    s = Service.objects.all().filter(ip=i)
    u = host.hostupdate_set.all()    
    swporttotal = swport.count()
    itotal = i.count()
    stotal = s.count()
    utotal = u.count()
    title = "Relatório do equipamento"
    return render_to_pdf(
            'ace/reports/hostdetailreport.html',
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
    i = Ip.objects.all()
    total = i.count()
    title = "Relatório de IPs"
    return render_to_pdf(
            'ace/reports/ipreport.html',
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
    s = Service.objects.all()
    total = s.count()
    title = "Relatório de serviços"
    return render_to_pdf(
            'ace/reports/servicereport.html',
            {
                'pagesize':'A4',
                'mylist': s,
                'total': total,
                'org':org,
                'title':title
            }
        )	





@login_required(login_url='/login/')
@permission_required('ace.view_phone',raise_exception=True)
def pwreport(request):
    p = Phone.objects.filter(password=True)
    total = p.count()
    title = "Relatório de senhas"
    return render_to_pdf(
            'ace/reports/pwreport.html',
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
    rack = Rack.objects.get(pk=rack_id)
    p = Netpoint.objects.filter(rack=rack)
    total = p.count()
    title ="Relatório de rack"
    return render_to_pdf(
            'ace/reports/rackreport.html',
            {
                'pagesize':'A4',
                'mylist': p,
                'total': total,
                'title':title,
                'rack':rack,
                'org':org,
            }
        )      

